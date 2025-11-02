from django.shortcuts import render
from .forms import FlightSearchForm
from .scraper import scrape_alibaba_flights

def home(request):
    flights = []
    if request.method == 'POST':
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            departing = data['departing']
            returning = data.get('returning')

            print("🟢 Calling scraper with:", departing, returning)

            flights = scrape_alibaba_flights(
                origin_code=data['origin'],
                dest_code=data['destination'],
                depart_date=departing,
                return_date=returning,
                headless=False,  # 🚨 برای تست فعلاً headless نباشه
            )
    else:
        form = FlightSearchForm()

    return render(request, 'main/home.html', {'form': form, 'flights': flights})