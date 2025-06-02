from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import StudyGroup, StudySession, UserProfile
from .forms import StudyGroupForm

def home(request):
    """
    Home page view for the study group platform
    """
    return render(request, 'home.html')

def groups_list(request):
    """
    Display all study groups
    """
    search_query = request.GET.get('search', '')
    subject_filter = request.GET.get('subject', '')

    groups = StudyGroup.objects.all()

    if search_query:
        groups = groups.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if subject_filter:
        groups = groups.filter(subject=subject_filter)

    subjects = StudyGroup.SUBJECT_CHOICES

    context = {
        'groups': groups,
        'subjects': subjects,
        'search_query': search_query,
        'subject_filter': subject_filter,
    }
    return render(request, 'groups/groups_list.html', context)

def group_detail(request, pk):
    """
    Display group details
    """
    group = get_object_or_404(StudyGroup, pk=pk)
    upcoming_sessions = group.sessions.filter(date_time__gte=timezone.now())[:3]

    context = {
        'group': group,
        'upcoming_sessions': upcoming_sessions,
        'is_member': request.user in group.members.all() if request.user.is_authenticated else False,
    }
    return render(request, 'groups/group_detail.html', context)

@login_required
def join_group(request, pk):
    """
    Join a study group
    """
    group = get_object_or_404(StudyGroup, pk=pk)

    if request.user not in group.members.all():
        if group.member_count < group.max_members:
            group.members.add(request.user)
            messages.success(request, f'You have successfully joined {group.name}!')
        else:
            messages.error(request, 'This group is full.')
    else:
        messages.info(request, 'You are already a member of this group.')

    return redirect('group_detail', pk=pk)

@login_required
def create_group(request):
    """
    Create a new study group
    """
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            # Add creator as first member
            group.members.add(request.user)
            messages.success(request, f'Study group "{group.name}" created successfully!')
            return redirect('group_detail', pk=group.pk)
    else:
        form = StudyGroupForm()

    context = {
        'form': form,
        'page_title': 'Create New Study Group'
    }
    return render(request, 'groups/create_group.html', context)

def calendar_view(request):
    """
    Display calendar with study sessions
    """
    # Get current month's sessions
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    if today.month == 12:
        end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

    sessions = StudySession.objects.filter(
        date_time__date__range=[start_of_month, end_of_month]
    )

    if request.user.is_authenticated:
        user_sessions = sessions.filter(
            Q(group__members=request.user) | Q(organizer=request.user)
        ).distinct()
    else:
        user_sessions = sessions.none()

    context = {
        'sessions': sessions,
        'user_sessions': user_sessions,
        'current_month': today.strftime('%B %Y'),
    }
    return render(request, 'calendar/calendar.html', context)

@login_required
def profile_view(request):
    """
    Display user profile
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_groups = request.user.joined_groups.all()
    created_groups = request.user.created_groups.all()
    upcoming_sessions = StudySession.objects.filter(
        Q(group__members=request.user) | Q(organizer=request.user),
        date_time__gte=timezone.now()
    ).distinct()[:5]

    context = {
        'profile': profile,
        'user_groups': user_groups,
        'created_groups': created_groups,
        'upcoming_sessions': upcoming_sessions,
    }
    return render(request, 'profile/profile.html', context)

def register_view(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            # Create user profile
            UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
