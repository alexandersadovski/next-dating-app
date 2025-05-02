from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST
from next.messaging.forms import MessageForm
from next.messaging.models import Message

UserModel = get_user_model()


@login_required
@require_GET
def show_chats(request):
    user = request.user

    conversations = Message.objects.filter(
        Q(sender=user, deleted_by_sender=False) | Q(receiver=user, deleted_by_receiver=False)
    ).order_by('-timestamp')

    unique_chats = {}
    for conversation in conversations:
        other_user_id = conversation.receiver.id if conversation.sender == user else conversation.sender.id

        if other_user_id not in unique_chats:
            unique_chats[other_user_id] = {
                'user': conversation.receiver if conversation.sender == user else conversation.sender,
                'last_message': conversation,
            }
    chats = list(unique_chats.values())

    is_chat_new = False
    receiver = None
    chat_id = request.GET.get('chat_id')
    if chat_id and int(chat_id) not in unique_chats:
        is_chat_new = True
        receiver = get_object_or_404(UserModel, id=chat_id)
    data = {'is_chat_new': is_chat_new, 'receiver': receiver}

    return render(request, 'dashboard/chats.html', {'chats': chats, 'data': data})


@login_required
@require_GET
def show_chat_messages(request, chat_id: int):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Invalid request')

    user = request.user
    matched_user = get_object_or_404(UserModel, id=chat_id)

    messages = Message.objects.filter(
        (
                Q(sender=user, receiver=matched_user, deleted_by_sender=False) |
                Q(sender=matched_user, receiver=user, deleted_by_receiver=False)
        )
    ).order_by('timestamp')

    form = MessageForm(initial={'receiver': matched_user})

    return render(request, 'dashboard/show-chat-messages.html', {
        'form': form,
        'messages': messages,
        'matched_user': matched_user,
    })


@login_required
@require_POST
def send_message(request):
    form = MessageForm(request.POST)

    if form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.save()

        message_html = render_to_string('dashboard/message.html', {
            'message': message,
            'request': request,
        })

        return JsonResponse({'message_html': message_html})
    else:
        return JsonResponse({'error': form.errors.as_json()}, status=400)


@login_required
@require_POST
def delete_chat(request, chat_id: int):
    user = request.user
    other_user = get_object_or_404(UserModel, id=chat_id)

    Message.objects.filter(sender=user, receiver=other_user).update(deleted_by_sender=True)
    Message.objects.filter(sender=other_user, receiver=user).update(deleted_by_receiver=True)

    conversations = Message.objects.filter(
        Q(sender=user, deleted_by_sender=False) | Q(receiver=user, deleted_by_receiver=False)
    ).order_by('-timestamp')

    is_conversations = True
    if not conversations:
        is_conversations = False

    return JsonResponse({'success': True, 'is_conversations': is_conversations})
