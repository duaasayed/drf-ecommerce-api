from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer, OrderTracking
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerified, OrdersPermissions
from rest_framework.decorators import action
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


class OrderViewset(ModelViewSet):
    queryset = Order.objects.prefetch_related(
        'order_products__product__colors__images').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsVerified, OrdersPermissions]

    def get_queryset(self):
        auth_user = self.request.user.customer
        return self.queryset.filter(customer=auth_user)

    @action(detail=True, methods=['GET'])
    def track(self, request, pk=None):
        order = self.get_object()
        serializer = OrderTracking(order.history, many=True)
        return Response(serializer.data)


def generate_invoices(request, pk=None):
    order = Order.objects.prefetch_related('order_products').get(pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{order.id}.pdf'
    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(0.5 * inch, 10.5 * inch, "Invoice")
    p.setFont("Helvetica", 12)
    p.drawString(0.5 * inch, 10.0 * inch, f"Order ID: {order.id}")
    p.drawString(0.5 * inch, 9.5 * inch, f"Date: {order.placed_at}")
    p.drawString(0.5 * inch, 9.0 * inch,
                 f"Purchaser: {order.customer.get_full_name()}")
    p.drawString(0.5 * inch, 8.5 * inch, f"Address: {order.address}")

    data = [
        ['Product', 'Price', 'Quantity', 'Total']
    ]
    for item in order.order_products.all():
        data.append([item.product.title, item.price,
                     item.quantity, item.total_price])
        table = Table(data)

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(table_style)

    table.wrapOn(p, 0, 0)
    table_width, table_height = table.wrap(7 * inch, 4 * inch)
    table.drawOn(p, (letter[0] - table_width) /
                 2, 7 * inch - table_height)

    total_price = order.total_price

    p.setFont("Helvetica-Bold", 12)
    p.drawString(6.5 * inch, 0.5 * inch, f"Total: ${total_price}")

    p.showPage()
    p.save()

    return response
