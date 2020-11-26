from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def corona_data(request):

    corona_html = requests.get("https://www.mygov.in/covid-19")
    soup = BeautifulSoup(corona_html.content, 'html.parser')
    state_wise_data = soup.find_all('div', class_='views-row')
    information = soup.find('div', class_='information_row')
    info = {
        'update_data': information.find('div', class_='info_title').find('span').string,
        'active_case': information.find('div', class_='active-case').find('span', class_='icount').string,
        'discharge': information.find('div', class_='discharge').find('span', class_='icount').string,
        'death': information.find('div', class_='death_case').find('span', class_='icount').string
    }

    corona_info = [
        {
            "state_name": state.find_all('span', class_='st_name')[0].string,
            "confirm_case": state.find_all('div', class_='tick-confirmed')[0].find_all('small')[0].string,
            "active_case": state.find_all('div', class_='tick-active')[0].find_all('small')[0].string,
            "discharge": state.find_all('div', class_='tick-discharged')[0].find_all('small')[0].string,
            "death": state.find_all('div', class_='tick-death')[0].find_all('small')[0].string
        } for state in state_wise_data
    ]

    context = {
        'corona_info': info,
        'data': sorted(corona_info, key=lambda i: int(''.join(i['confirm_case'].replace(',', ''))), reverse=True)
    }

    return render(request, 'coronainfo/index.html', context)
