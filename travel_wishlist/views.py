from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf.urls import url
from .models import Place
from .forms import NewPlaceForm


def place_details(request, place_pk):

    place = get_object_or_404(Place, pk=place_pk)
    return render(request, 'travel_wishlist/place_detail.html', {'place':place } )


def place_is_visited(request, place_pk):

    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()

    return redirect('place_list')



def place_list(request):

    # If a POST request, this must be from user clicking Add button
    # in the form. Check if new place is valid and add to list, then
    # redirect to 'place_list' route - which ends up creating a GET
    # request for this same method.
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save()
        if form.is_valid():
            place.save()
            return redirect('place_list')

    # If not a POST request, or the form is not valid, display the page
    # with the form, and place list
    places = Place.objects.filter(visited=False)
    form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places' : places, 'form' : form})


def places_visited(request):

    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited':visited})
