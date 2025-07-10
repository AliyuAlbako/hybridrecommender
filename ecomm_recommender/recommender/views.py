from django.shortcuts import render
from .models import Product
from .serializer import ProductSerializer
from .recommendation_engine import content_based
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .recommendation_engine.content_based import get_content_based_recommendations
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q



def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products, 'query': query})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    recommendations = get_content_based_recommendations(product_id, top_n=5)

    return render(request, 'product_detail.html', {
        'product': product,
        'recommendations': recommendations
    })


@csrf_exempt
def product_suggestions(request):
    query = request.GET.get('term', '')
    if query:
        products = Product.objects.filter(name__icontains=query)[:5]
        results = [{'id': p.id, 'name': p.name} for p in products]
    else:
        results = []
    return JsonResponse(results, safe=False)



