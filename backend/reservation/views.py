from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from calendar import month_name
from reservation.calendar import Calendar
from datetime import date, datetime, timedelta
from reservation.models import Reservation
from rooms.models import Room
from django.db import transaction


@login_required
def reservation_year(request, room_slug, curr_year):
    # Pagination
    current_year = datetime.now().year
    paginator_years = [current_year-1, current_year, current_year+1]
    paginator = Paginator(paginator_years, 1)
    year = request.GET.get('year')
    if year is None:
        year = current_year
    paged_year = paginator.get_page(year)

    # Display
    calendar = [[Calendar().itermonthdays4(curr_year, i), i, month_name[i]] for i in range(1, 13)]
    context = {
        'room_slug': room_slug,
        'curr_year': curr_year,
        'dates': Calendar(),
        'current_year': current_year,
        'paged_year': paged_year,
        'paginator_years': paginator_years,
        'year': int(year),
        'calendar': calendar,
    }

    return render(request, 'reservation/year.html', context)


@login_required
def reservation_day(request, room_slug, year, month, day):
    user_group = request.user.groups.get().name
    room = Room.objects.get(room_slug=room_slug)
    room_slug = room_slug
    time_choices = Reservation.TIME_CHOICES
    reservations = []
    for i in range(1, len(Reservation.TIME_CHOICES)+1):
        try:
            reservation_holder = Reservation.objects.get(room=room,
                                                         year_slug=year,
                                                         month_slug=month,
                                                         day_slug=day,
                                                         time=i)
            reservations += [[True,
                              reservation_holder,
                              time_choices[i-1],
                              reservation_holder.user.groups.get().name,
                              ]]
        except ObjectDoesNotExist:
            reservations += [[False,
                              time_choices[i-1],
                              True if datetime.now() < datetime(year,
                                                                month,
                                                                day,
                                                                6 + int(time_choices[i-1][0]) * 2)
                              else False]]
    if request.method == 'POST':
        if 'create_reservation' in request.POST:
            # if user has other reservation in the same time
            try:
                Reservation.objects.get(user=request.user,
                                        year_slug=year,
                                        month_slug=month,
                                        day_slug=day,
                                        time=request.POST['time'])
                messages.error(request, 'You already have another room reserved in the same time!')
                return redirect('reservation_day', room_slug, year, month, day)

            # if user has no other reservation in the same time
            except ObjectDoesNotExist:
                # check if nobody reserved this since last response
                with transaction.atomic():
                    # if someone reserved this since last response
                    try:
                        Reservation.objects.get(room=room,
                                                year_slug=year,
                                                month_slug=month,
                                                day_slug=day,
                                                time=request.POST['time'])
                        # do not reserve and show message
                        messages.error(request, 'Someone else just reserved this room!')
                        return redirect('reservation_day', room_slug, year, month, day)

                    # if nobody reserved this since last response
                    except ObjectDoesNotExist:
                        # create new reservation
                        new_reservation = Reservation(user=request.user,
                                                      room=room,
                                                      date=date(year, month, day),
                                                      time=request.POST['time'])
                        new_reservation.save()
                        # show message
                        messages.success(request, 'Room reserved!')
                        return redirect('reservation_day', room_slug, year, month, day)

        elif 'remove_reservation' in request.POST:
            # if nobody forced reservation of this room since last response
            try:
                with transaction.atomic():
                    # remove reservation as requested
                    remove_reservation = Reservation.objects.get(user=request.user,
                                                                 room__room_slug=room_slug,
                                                                 year_slug=year,
                                                                 month_slug=month,
                                                                 day_slug=day,
                                                                 time=request.POST['time'])
                    remove_reservation.delete()
                    messages.success(request, 'Reservation removed!')
                    return redirect('reservation_day', room_slug, year, month, day)

            # if someone forced reservation of this room since last response
            except ObjectDoesNotExist:
                # do not remove reservation and show message
                messages.success(request, 'Reservation removed!')
                return redirect('reservation_day', room_slug, year, month, day)

        elif 'force_reservation' in request.POST:
            # if user has other reservation in the same time
            try:
                Reservation.objects.get(user=request.user,
                                        year_slug=year,
                                        month_slug=month,
                                        day_slug=day,
                                        time=request.POST['time'])
                # do not force reservation and show message
                messages.success(request, 'You already have another room reserved in the same time!')
                return redirect('reservation_day', room_slug, year, month, day)

            # if user has no other reservation in the same time
            except ObjectDoesNotExist:
                # if nobody deleted reservation of this room since last response
                try:
                    with transaction.atomic():
                        forced_reservation = Reservation.objects.get(reservation_slug=request.POST['force_reservation'])
                        # if reservation is upcoming in 24 hours
                        restriction_time = datetime(year,
                                                    month,
                                                    day,
                                                    6 + int(forced_reservation.reservation_slug[-1]) * 2)
                        restriction_time = restriction_time - timedelta(days=1)
                        if datetime.now() > restriction_time:
                            messages.success(request, 'Reservation cannot be forced less than 24 hours before!')
                            return redirect('reservation_day', room_slug, year, month, day)

                        # check if nobody with higher priority forced reservation of this room since last response
                        # Staff group can force reservation on Student and Lecturer groups
                        if user_group == 'Staff':
                            if forced_reservation.user.groups.get().name in "Student Lecturer":
                                forced_reservation.user = request.user
                                forced_reservation.save()
                                messages.success(request, 'Reservation forced!')
                                return redirect('reservation_day', room_slug, year, month, day)
                            else:
                                messages.success(request, 'Someone else with higher priority just forced this!')
                                return redirect('reservation_day', room_slug, year, month, day)

                        # Local Admin group can force reservation on Student, Lecturer and Staff groups
                        elif user_group == 'Local Admin':
                            if forced_reservation.user.groups.get().name in "Student Lecturer Staff":
                                forced_reservation.user = request.user
                                forced_reservation.save()
                                messages.success(request, 'Reservation forced!')
                                return redirect('reservation_day', room_slug, year, month, day)
                            else:
                                messages.success(request, 'Someone else with higher priority just forced this!')
                                return redirect('reservation_day', room_slug, year, month, day)

                        # Admin group can force reservation on every group
                        elif user_group == 'Admin':
                            forced_reservation.user = request.user
                            forced_reservation.save()
                            messages.success(request, 'Reservation forced!')
                            return redirect('reservation_day', room_slug, year, month, day)

                # if someone deleted reservation of this room since last response
                except ObjectDoesNotExist:
                    # do not force reservation and show message
                    messages.success(request, 'Someone just removed reservation of this room!')
                    return redirect('reservation_day', room_slug, year, month, day)

    context = {
        'user_group': user_group,
        'room_slug': room_slug,
        'reservations': reservations,
        'time_choices': time_choices,
        'current_year': datetime.now().year,
    }
    return render(request, 'reservation/day.html', context)
