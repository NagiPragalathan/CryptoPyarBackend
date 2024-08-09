from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from base.models import Chat, Message, Profile
from .WebThree import send_chat_to_blockchain

def chat_room(request, address, endpoint):
    chat, created = Chat.objects.get_or_create(endpoint=endpoint, address=address)
    all_chats = Chat.objects.filter(address=address)

    chat_profiles = []
    for chat in all_chats:
        try:
            profile = Profile.objects.get(address=chat.address)
            endpoint_p = ""
            for i in Chat.objects.filter(address=profile.address):
                if i.address == address:
                    endpoint_p = i.endpoint
            profile.redirect_endpoint = endpoint_p
            chat_profiles.append(
                profile,
            )
        except Profile.DoesNotExist:
            pass
    my_profile = Profile.objects.get(address=address)
    if request.method == 'POST':
        content = request.POST.get('content')
        sender_address = request.POST.get('sender_address')
        if content and sender_address:
            hashval = send_chat_to_blockchain(str(chat.id), sender_address, content, endpoint)
            print(hashval)
            Message.objects.create(chat_id=chat.id, content=content, sender_address=sender_address, endpoint=endpoint, transaction=hashval, timestamp=timezone.now())
            return JsonResponse({'status': 'ok'})
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        messages = Message.objects.filter(endpoint=endpoint).order_by('timestamp')
        for i in messages:
            i.name = Profile.objects.get(address=i.sender_address).name
        return JsonResponse({
            'messages': [
                {
                    'sender_address': message.sender_address,
                    'content': message.content,
                    'transaction': message.transaction,  # Include transaction data
                } for message in messages
            ]
        })
    else:
        messages = Message.objects.filter(endpoint=endpoint,).order_by('timestamp')
        return render(request, 'chat.html', {'chat': chat, 'messages': messages, 'address': address, 'chat_list': list(set(chat_profiles)), "my_profile": my_profile})
