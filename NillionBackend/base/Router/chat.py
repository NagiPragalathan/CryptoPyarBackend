from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from base.models import Chat, Message, Profile
from .WebThree import send_chat_to_blockchain
import requests

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
            Aptos = store_message(sender_address, content, "1", "0x8144e9a42fed8ff976703c0c2d24b410f86f004770a32876aed4172b303e020b")
            print(str(hashval)+"\nAptos: "+str(Aptos))
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


def store_message(to_address, message_content, timestamp, private_key):
    # Define the API endpoint URL
    api_url = "https://vortex-server-three.vercel.app/api/entry-with-private"
    
    # Data to be sent to the API
    data = {
        "toaddress": to_address,
        "messagecontent": message_content,
        "timestamp": timestamp,
        "privateKey": private_key
    }
    
    # Send the POST request to the API
    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()  # Raise an error for bad status codes

        # Print the response from the server
        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
