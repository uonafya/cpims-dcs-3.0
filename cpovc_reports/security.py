"""Cert generation."""
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import Flowable
from reportlab.lib.pagesizes import A4


class BarCode(Flowable):
    """Barcode class."""

    def __init__(self, value="1234567890", ratio=2.1):
        """Init and store rendering value."""
        Flowable.__init__(self)
        self.value = value
        self.ratio = ratio

    def wrap(self, availwidth, availheight):
        """Make the barcode fill the width while maintaining the ratio."""
        self.width = availwidth
        self.height = self.ratio * availheight
        return self.width, self.height

    def draw(self):
        """Flowable canvas."""
        # w = float(self.width)
        # h = float(self.height)

        a4width, a4height = A4
        """
        d = Drawing(w, h, transform=[w / bar_width, 0, 0,
                                     h / bar_height, 0, 0])
        d.add(bar_code)

        renderPDF.draw(d, self.canv, 0, 0)
        """
        qr_code = qr.QrCodeWidget(self.value)
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        d = Drawing(65, 65, transform=[65. / width, 0, 0, 65. / height, 0, 0])
        d.add(qr_code)
        renderPDF.draw(d, self.canv, 30, height - 90)
