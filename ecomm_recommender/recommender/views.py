from django.shortcuts import render, get_object_or_404
from .models import Product, Rating
from django.http import JsonResponse
from django.db.models import Q, Avg
from .recommendation.hybrid import get_hybrid_recommendations
from django.views.decorators.csrf import csrf_exempt


def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    # annotate each product with avg_rating
    products = products.annotate(avg_rating=Avg('rating__rating'))

    return render(request, 'product_list.html', {
        'products': products,
        'query': query
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # compute avg rating for this product
    product.avg_rating = Rating.objects.filter(product=product).aggregate(
        Avg("rating")
    )["rating__avg"] or 0

    # for demo, user_id left None (unauthenticated)
    recommendations = get_hybrid_recommendations(None, product_id, top_n=5, alpha=0.6)

    return render(request, 'product_detail.html', {
        'product': product,
        'recommendations': recommendations
    })


# API endpoint for hybrid recommendations (JSON)
def api_hybrid_recommendations(request, product_id):
    recs = get_hybrid_recommendations(None, product_id, top_n=8, alpha=0.6)
    data = []
    for p in recs:
        avg_rating = Rating.objects.filter(product=p).aggregate(
            Avg("rating")
        )["rating__avg"] or 0
        data.append({
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': str(p.price) if p.price else None,
            'image_url': p.image_url,
            'source': p.source,
            'product_url': p.product_url,
            'avg_rating': round(avg_rating, 1),
        })
    return JsonResponse({'recommendations': data})


@csrf_exempt
def product_suggestions(request):
    query = request.GET.get('term', '')
    if query:
        products = Product.objects.filter(name__icontains=query)[:5]
        results = [{'id': p.id, 'name': p.name} for p in products]
    else:
        results = []
    return JsonResponse(results, safe=False)
