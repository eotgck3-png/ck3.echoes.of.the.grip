"""Synthetic-image tests for docs/tools/convert_art.py.

Every profile's output size and DDS header, alpha handling, law blackening and margin,
the black key (flood fill from the edges: no interior holes, no see-through outline),
fit without stretching, trait backdrop placement and tone, and batch mode.
Run: python -m pytest -q docs/tools/tests
"""
import io
import os
import sys
import unittest

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _testutil import tempdir  # noqa: E402
import convert_art as C  # noqa: E402


def _save(im, d, name):
    p = os.path.join(d, name)
    im.save(p)
    return p


def _read(path):
    return np.asarray(Image.open(path).convert("RGBA"))


def _painted(size=(300, 300), alpha=True):
    """A colourful disc on transparent (or black) ground."""
    im = Image.new("RGBA" if alpha else "RGB", size, (0, 0, 0, 0) if alpha else (0, 0, 0))
    d = ImageDraw.Draw(im)
    w, h = size
    d.ellipse((w * 0.2, h * 0.2, w * 0.8, h * 0.8), fill=(200, 120, 40, 255) if alpha else (200, 120, 40))
    d.rectangle((w * 0.4, h * 0.4, w * 0.6, h * 0.6), fill=(40, 160, 200, 255) if alpha else (40, 160, 200))
    return im


def _scene(size=(2000, 1000)):
    a = np.linspace(0, 1, size[0])[None, :, None] * np.ones((size[1], 1, 1))
    rgb = np.concatenate([a * 220, (1 - a) * 180, np.full_like(a, 90)], axis=2)
    return Image.fromarray(rgb.astype(np.uint8), "RGB")


class Profiles(unittest.TestCase):
    def test_every_profile_size_and_header(self):
        with tempdir() as d:
            src_rgba = _save(_painted(), d, "icon.png")
            src_rgb = _save(_scene(), d, "scene.jpg")
            for name, prof in C.PROFILES.items():
                src = src_rgb if not prof.alpha else src_rgba
                dst = os.path.join(d, name + ".dds")
                r = C.convert(src, dst, name)
                w, h, fmt, mips = C.read_dds_header(dst)
                self.assertEqual((w, h), prof.size, name)
                self.assertEqual(fmt, prof.fmt, name)
                self.assertEqual(mips, C.mip_count(w, h) if prof.mips else 0, name)
                self.assertEqual(Image.open(dst).size, prof.size, name)  # Pillow reads it back
                self.assertEqual(r["out"], prof.size)

    def test_file_length_matches_mip_chain(self):
        with tempdir() as d:
            src = _save(_painted(), d, "i.png")
            dst = os.path.join(d, "m.dds")
            C.convert(src, dst, "modifier")
            expect = 128 + sum(max(1, 60 >> i) ** 2 * 4 for i in range(6))
            self.assertEqual(os.path.getsize(dst), expect)
            dst = os.path.join(d, "inn.dds")
            C.convert(_save(_scene((400, 300)), d, "s.png"), dst, "innovation")
            blocks = 0
            w, h = 180, 120
            for i in range(8):
                lw, lh = max(1, w >> i), max(1, h >> i)
                blocks += ((lw + 3) // 4) * ((lh + 3) // 4)
            self.assertEqual(os.path.getsize(dst), 128 + blocks * 8)

    def test_bgra_channel_order(self):
        im = Image.new("RGBA", (4, 4), (10, 20, 30, 40))
        data = C.dds_bytes(im, "BGRA", False)
        self.assertEqual(data[128:132], bytes([30, 20, 10, 40]))


class Alpha(unittest.TestCase):
    def test_icon_keeps_transparency(self):
        with tempdir() as d:
            dst = os.path.join(d, "o.dds")
            C.convert(_save(_painted(), d, "i.png"), dst, "interaction")
            a = _read(dst)
            self.assertEqual(a[0, 0, 3], 0)
            self.assertEqual(a[60, 60, 3], 255)

    def test_rgb_profile_is_opaque(self):
        with tempdir() as d:
            dst = os.path.join(d, "o.dds")
            r = C.convert(_save(_painted((500, 200)), d, "i.png"), dst, "decision")
            self.assertTrue((_read(dst)[..., 3] == 255).all())
            self.assertTrue(any("composited" in w for w in r["warnings"]))

    def test_innovation_fills_transparency_with_vignette(self):
        with tempdir() as d:
            dst = os.path.join(d, "o.dds")
            r = C.convert(_save(_painted((300, 200)), d, "i.png"), dst, "innovation")
            a = _read(dst)
            self.assertTrue((a[..., 3] == 255).all())
            self.assertGreater(int(a[60, 5, :3].sum()), 0)   # vignette, not pure black
            self.assertFalse(r["warnings"])


class Law(unittest.TestCase):
    def test_blackened_and_margin(self):
        with tempdir() as d:
            dst = os.path.join(d, "law.dds")
            r = C.convert(_save(_painted((96, 96)), d, "l.png"), dst, "law")
            a = _read(dst)
            vis = a[..., 3] > 0
            self.assertTrue(vis.any())
            self.assertTrue((a[vis][:, :3] == 0).all())
            ys, xs = np.nonzero(a[..., 3] >= 8)
            self.assertGreaterEqual(min(xs.min(), ys.min(), 95 - xs.max(), 95 - ys.max()), 8)
            self.assertFalse(r["warnings"])

    def test_full_bleed_source_is_shrunk_inside_margin(self):
        with tempdir() as d:
            im = Image.new("RGBA", (200, 200), (255, 0, 0, 255))
            dst = os.path.join(d, "law.dds")
            C.convert(_save(im, d, "full.png"), dst, "law")
            a = _read(dst)
            self.assertEqual(a[4, 4, 3], 0)
            self.assertEqual(a[48, 48, 3], 255)


class KeyBlack(unittest.TestCase):
    def _source(self):
        """Grey tile on black: a black outline ring that touches the background, a black
        disc inside the tile (interior black that must stay opaque), and a 2 px black
        crack running from the outside into the tile (the d0e5e2c leak)."""
        im = Image.new("RGB", (400, 400), (0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle((80, 80, 320, 320), fill=(0, 0, 0))            # outline (black)
        d.rectangle((86, 86, 314, 314), fill=(120, 130, 125))      # tile
        d.ellipse((170, 170, 230, 230), fill=(0, 0, 0))            # interior black
        d.rectangle((80, 199, 140, 200), fill=(0, 0, 0))           # crack from the edge
        rng = np.random.default_rng(1)
        a = np.asarray(im).astype(int) + rng.integers(0, 10, (400, 400, 3))  # JPG-ish noise
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")

    def test_no_interior_holes(self):
        out = np.asarray(C.key_black(self._source()))[..., 3]
        self.assertEqual(out[5, 5], 0)                     # background keyed
        self.assertEqual(out[200, 200], 255)               # interior black disc kept
        self.assertEqual(out[200, 110], 255)               # crack sealed, not see-through
        self.assertTrue((out[90:311, 90:311] == 255).all())  # whole tile interior opaque

    def test_soft_outer_edge_only(self):
        out = np.asarray(C.key_black(self._source(), close_px=3))[..., 3]
        partial = (out > 0) & (out < 255)
        self.assertTrue(partial.any())                     # feathered edge exists
        ys, xs = np.nonzero(partial)
        inside = (xs > 86) & (xs < 314) & (ys > 86) & (ys < 314)
        self.assertFalse(inside.any())                     # none inside the shape

    def test_key_black_through_cli_profile(self):
        with tempdir() as d:
            src = os.path.join(d, "k.jpg")
            self._source().save(src, quality=90)
            dst = os.path.join(d, "k.dds")
            r = C.convert(src, dst, "interaction", key=True)
            a = _read(dst)
            self.assertEqual(a[2, 2, 3], 0)
            self.assertEqual(a[60, 60, 3], 255)
            self.assertFalse(r["warnings"])

    def test_jpg_icon_without_key_warns(self):
        with tempdir() as d:
            src = os.path.join(d, "k.jpg")
            self._source().save(src)
            r = C.convert(src, os.path.join(d, "k.dds"), "modifier")
            self.assertTrue(any("--key-black" in w for w in r["warnings"]))


class Geometry(unittest.TestCase):
    def test_cover_never_stretches(self):
        im = Image.new("RGB", (1000, 1000), (0, 0, 0))
        ImageDraw.Draw(im).ellipse((300, 300, 700, 700), fill=(255, 255, 255))
        out, _ = C.fit(im, (1100, 440), "cover")
        a = np.asarray(out)[..., 0] > 128
        ys, xs = np.nonzero(a)
        self.assertAlmostEqual((xs.max() - xs.min()) / (ys.max() - ys.min()), 1.0, delta=0.03)

    def test_contain_pads(self):
        im = Image.new("RGBA", (200, 100), (255, 0, 0, 255))
        out, _ = C.fit(im, (60, 60), "contain")
        a = np.asarray(out)
        self.assertEqual(a[0, 30, 3], 0)
        self.assertEqual(a[30, 30, 3], 255)

    def test_crop(self):
        with tempdir() as d:
            im = Image.new("RGBA", (200, 100), (0, 0, 0, 0))
            ImageDraw.Draw(im).rectangle((100, 0, 199, 99), fill=(255, 0, 0, 255))
            dst = os.path.join(d, "o.dds")
            C.convert(_save(im, d, "c.png"), dst, "modifier", crop_box=(100, 0, 100, 100), do_tone=False)
            self.assertTrue((_read(dst)[..., 3] == 255).all())
            with self.assertRaises(ValueError):
                C.convert(_save(im, d, "c.png"), dst, "modifier", crop_box=(150, 0, 100, 100))


class Trait(unittest.TestCase):
    def test_backdrop_lands_on_92px_square_and_tone(self):
        im = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle((100, 80, 399, 379), fill=(30, 150, 150, 255))     # teal tile, 300 px
        d.ellipse((180, 160, 320, 300), fill=(220, 180, 60, 255))     # object
        with tempdir() as td:
            dst = os.path.join(td, "t.dds")
            C.convert(_save(im, td, "t.png"), dst, "trait")
            a = _read(dst)
            ys, xs = np.nonzero(a[..., 3] > 128)
            self.assertLessEqual(abs(xs.min() - 14), 1)
            self.assertLessEqual(abs(xs.max() - 105), 1)
            self.assertLessEqual(abs(ys.min() - 15), 1)
            self.assertLessEqual(abs(ys.max() - 106), 1)
            _, _, s, v = C.measure(Image.fromarray(a, "RGBA"))
            self.assertAlmostEqual(s, 0.32, delta=0.02)
            self.assertAlmostEqual(v, 0.33, delta=0.02)

    def test_interaction_saturation_cut_at_most_20pct(self):
        im = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((10, 10, 110, 110), fill=(220, 40, 40, 255))  # S ~0.82
        out = C.tone(im, C.PROFILES["interaction"])
        s0 = C.measure(im)[2]
        s1 = C.measure(out)[2]
        self.assertAlmostEqual(s1 / s0, 0.8, delta=0.02)

    def test_no_tone_leaves_pixels(self):
        with tempdir() as d:
            im = _scene((1100, 440))
            src = _save(im, d, "s.png")
            dst = os.path.join(d, "s.dds")
            r = C.convert(src, dst, "decision", do_tone=False)
            self.assertAlmostEqual(r["val"][0], r["val"][1], delta=0.01)
            r = C.convert(src, dst, "decision")
            self.assertLessEqual(r["val"][1], 0.215)


class Batch(unittest.TestCase):
    def test_csv(self):
        with tempdir() as d:
            _save(_painted(), d, "a.png")
            _save(_scene(), d, "b.png")
            with open(os.path.join(d, "jobs.csv"), "w", encoding="utf-8") as f:
                f.write("src,profile,dst,flags\n")
                f.write("a.png,modifier,out/a.dds,--no-tone\n")
                f.write('b.png,event_background,out/b.dds,"--crop 0,0,1000,1000 --fit contain"\n')
                f.write("missing.png,modifier,out/c.dds,\n")
            buf = io.StringIO()
            fails = C.run_batch(os.path.join(d, "jobs.csv"), out=buf)
            self.assertEqual(fails, 1)
            self.assertEqual(C.read_dds_header(os.path.join(d, "out", "a.dds"))[:2], (60, 60))
            self.assertEqual(C.read_dds_header(os.path.join(d, "out", "b.dds"))[:2], (1592, 848))
            self.assertIn("FAILED missing.png", buf.getvalue())


def _green_square(size=200):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(im).rectangle((20, 20, size - 20, size - 20), fill=(110, 140, 90, 255))
    return im


class Additions2026_10_12(unittest.TestCase):
    def test_badge_corners(self):
        with tempdir() as d:
            src = _save(_green_square(), d, "g.png")
            for direction, (cx, cy), (fx, fy) in (("up", (15, 14), (58, 58)), ("down", (47, 44), (1, 1))):
                dst = os.path.join(d, direction + ".dds")
                C.convert(src, dst, "modifier", badge=direction)
                a = _read(dst)
                self.assertEqual(a[cy, cx, 3], 255)          # inside the badge
                self.assertGreater(a[cy, cx, 1], a[cy, cx, 0])   # silhouette colour (green)
                self.assertEqual(a[fy, fx, 3], 0)            # far corner left clear

    def test_badge_needs_modifier(self):
        with tempdir() as d:
            with self.assertRaises(ValueError):
                C.convert(_save(_green_square(), d, "g.png"), os.path.join(d, "x.dds"), "law", badge="up")

    def test_law_marks_black_inside_margin(self):
        with tempdir() as d:
            src = _save(_painted((96, 96)), d, "l.png")
            plain = os.path.join(d, "plain.dds")
            C.convert(src, plain, "law", alpha_thresh=128)
            base = _read(plain)[..., 3]
            soft = np.count_nonzero((base > 0) & (base < 255))
            self.assertTrue(0 < soft < 0.2 * np.count_nonzero(base))  # flat body, 1 px AA edge
            for mark in C.LAW_MARKS:
                dst = os.path.join(d, mark + ".dds")
                r = C.convert(src, dst, "law", alpha_thresh=128, law_mark=mark)
                a = _read(dst)
                self.assertTrue((a[a[..., 3] > 0][:, :3] == 0).all())
                self.assertFalse(r["warnings"])
                self.assertGreater(np.count_nonzero(a[..., 3] != base), 50)

    def test_despeckle_and_threshold(self):
        im = _green_square(100)
        im.putpixel((2, 2), (255, 255, 255, 200))
        im.putpixel((5, 90), (255, 255, 255, 60))
        out, n = C.despeckle(im, 5)
        self.assertEqual(n, 2)
        a = np.asarray(C.alpha_threshold(im, 128))[..., 3]
        self.assertEqual(a[2, 2], 255)
        self.assertEqual(a[90, 5], 0)

    def test_key_luma_clears_enclosed_black(self):
        im = Image.new("RGB", (100, 100), (0, 0, 0))
        dr = ImageDraw.Draw(im)
        dr.ellipse((10, 10, 90, 90), fill=(150, 200, 150))
        dr.ellipse((40, 40, 60, 60), fill=(0, 0, 0))     # enclosed hole
        a = np.asarray(C.key_luma(im))
        self.assertEqual(a[50, 50, 3], 0)
        self.assertEqual(a[20, 50, 3], 255)

    def test_recolor_and_erase(self):
        im = Image.new("RGBA", (60, 60), (220, 210, 190, 255))
        ImageDraw.Draw(im).rectangle((20, 20, 40, 40), fill=(180, 30, 30, 255))
        out, n = C.recolor_red(im, (10, 10, 40, 40), (120, 140, 130))
        self.assertEqual(n, 21 * 21)
        px = out.getpixel((30, 30))
        self.assertLess(abs(px[0] - px[2]), 40)          # no longer red
        er = np.asarray(C.erase_polys(im, [[(0, 0), (20, 0), (0, 20)]], grow=1))
        self.assertEqual(er[2, 2, 3], 0)
        self.assertEqual(er[50, 50, 3], 255)


class FillHoles(unittest.TestCase):
    def test_upstream_keyed_interior_open_to_background(self):
        """A source whose dark interior was keyed out upstream, with the hole reaching the
        background through a narrow dark channel (so binary_fill_holes alone misses it).
        It must come back opaque and dark, and trim + contain must not clip the subject."""
        im = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        dr.ellipse((30, 30, 190, 190), fill=(150, 120, 90, 255))
        dr.rectangle((60, 60, 160, 160), fill=(20, 15, 10, 255))       # dark interior
        dr.ellipse((70, 70, 150, 150), fill=(0, 0, 0, 0))              # keyed out upstream
        dr.rectangle((106, 140, 114, 220), fill=(0, 0, 0, 0))          # channel to the edge
        out, n = C.fill_holes(im, 5)
        a = np.asarray(out)
        self.assertGreater(n, 4000)
        self.assertEqual(a[110, 110, 3], 255)
        self.assertLess(a[110, 110, :3].max(), 60)                     # dark tone, not paint
        self.assertEqual(a[5, 5, 3], 0)                                # background stays clear
        with tempdir() as d:
            dst = os.path.join(d, "i.dds")
            C.convert(_save(im, d, "i.png"), dst, "interaction", do_trim=True, margin=5,
                      fill_holes_px=5)
            al = _read(dst)[..., 3]
            ys, xs = np.nonzero(al > 0)
            self.assertEqual((xs.min(), ys.min()), (5, 5))             # nothing cut
            self.assertEqual((119 - xs.max(), 119 - ys.max()), (5, 5))
            self.assertEqual(al[60, 60], 255)


if __name__ == "__main__":
    unittest.main()
