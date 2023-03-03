from django.shortcuts import render, redirect
from django.db.models import Q

from django.core.mail import send_mail
from coursework3 import settings
from .forms import LogInUser, RegisterForm
from django.contrib.auth import login, authenticate

from .models import Account, Item, Bid, Question, Answer
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect, HttpResponse
import json

from django.shortcuts import render, redirect
from django.contrib import messages

from typing import Union


def profileupdate(request: HttpRequest, account_id: int) -> JsonResponse:
    user = Account.objects.get(id=account_id)

    if request.method == 'POST':
        print(request.FILES)

        if len(request.FILES) > 0:
            user.profileImage = request.FILES['image']
            user.save()
        else:
            return JsonResponse({'warn': 'No files were uploaded'}, status=400)

        return JsonResponse(specificUser.to_dict())


# function return either an HttpResponseRedirect object or an HttpResponse object - thats what the union part means.
def register(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    global specificUser
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = form.save()
            login(request, user)
            form = RegisterForm()
            # subject = "Welcome" + user.username
            # message = "Welcome to Fake eBay."
            # from_email = settings.EMAIL_HOST_USER
            # to_list = [user.email]
            # send_mail(subject, message, from_email,
            #           to_list, fail_silently=False)
            specificUser = Account.objects.get(email=email)

            return redirect('http://localhost:5173/')

    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


# function return either an HttpResponseRedirect object or an HttpResponse object - thats what the union part means.
def log_in(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    global specificUser
    if request.method == "POST":
        form = LogInUser(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                print("USER AUTHENTICAED:", request.user)
                specificUser = Account.objects.get(email=email)

                return redirect('http://localhost:5173/')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LogInUser()

    return render(request, 'registration/login.html', {'form': form})


def account_api(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        return JsonResponse({
            'SpecificUser': [
                specificUser.to_dict()
            ]
            # account in line 72 will show undefined without this line. idk why
        })


def accounts_api(request):
    if request.method == 'GET':
        return JsonResponse({
            'AllAccounts': [
                account.to_dict()
                for account in Account.objects.all()
            ]
        })


def user_api(request: HttpRequest, account_id: int) -> HttpResponseRedirect:
    user = Account.objects.get(id=account_id)

    if request.method == "GET":
        print(user)

        return JsonResponse(user.to_dict())

    if request.method == 'PUT':
        body = json.loads(request.body)
        updateUser = Account.objects.get(id=account_id)

        updateUser.email = body['email']
        updateUser.first_name = body['first_name']
        updateUser.last_name = body['last_name']

        updateUser.dOB = body['dOB']

        updateUser.phoneNumber = body['phoneNumber']
        updateUser.addressLine1 = body['addressLine1']
        updateUser.addressLine2 = body['addressLine2']
        updateUser.city = body['city']
        updateUser.postcode = body['postcode']
        updateUser.country = body['country']
        updateUser.save()

        return JsonResponse(
            updateUser.to_dict()
        )


def createItem(request: HttpRequest, account_id: int) -> JsonResponse:
    if request.method == 'GET':
        return JsonResponse({  # pass a dictionary that passes list of teams.
            'item': [
                item.to_dict()
                for item in Item.objects.filter(user=account_id)

            ]  # list of dictionaries
        })  # Now build ONLY one dictionary that contains the list of dictionaries.

    if request.method == 'POST':

        category = request.POST['category']
        image = request.FILES['image']
        title = request.POST['title']
        description = request.POST['description']
        startingPrice = request.POST['startingPrice']
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']

        loggedAccount = Account.objects.get(id=account_id)
        Item.objects.create(
            item_tag=category,
            user=loggedAccount,
            pictureOfItem=image,
            title=title,
            description=description,
            startingPrice=startingPrice,
            startDateTimeItem=startDate,
            endDateTimeItem=endDate,
        )
    return JsonResponse({
        "Success": "Item was created"
    })


def getItemDetail(request: HttpRequest, item_id: int) -> JsonResponse:
    if request.method == 'GET':

        item = Item.objects.get(id=item_id)

        return JsonResponse(
            item.to_dict()
        )

    if request.method == 'DELETE':
        item = Item.objects.get(id=item_id)
        item.delete()
        return JsonResponse({
            "Status": "Item deleted!"
        })


def addBid(request: HttpRequest, item_id: int) -> JsonResponse:
    if request.method == 'POST':
        body = json.loads(request.body)
        bidUser = body['bidUser']
        bidAmount = body['bidAmount']
        bidTime = body['bidTime']

        user = Account.objects.get(id=bidUser)
        item = Item.objects.get(id=item_id)

        Bid.objects.create(
            userIDFK=user,
            itemIDFK=item,
            bidAmount=bidAmount,
            dateTimeBids=bidTime,
        )

    return JsonResponse({
        "Status:": "Bid Created"
    })


def getBids(request: HttpRequest, item_id: int) -> JsonResponse:
    item = Item.objects.get(id=item_id)

    if request.method == "GET":
        return JsonResponse({  # pass a dictionary that passes list of teams.
            'bids': [
                bids.to_dict()
                for bids in Bid.objects.filter(itemIDFK=item)

            ]  # list of dictionaries
        })


def displayItems(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        return JsonResponse({
            'AllItems': [
                item.to_dict()
                for item in Item.objects.all()
            ]
        })


def question(request: HttpRequest, item_id: int) -> JsonResponse:
    if request.method == 'GET':
        item = Item.objects.get(id=item_id)
        return JsonResponse({
            'questions': [
                question.to_dict()
                for question in Question.objects.filter(itemFK=item)
            ]
        })

    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        questionUser = body['questionUser']
        userQuestion = body['userQuestion']
        questionTime = body['questionTime']

        user = Account.objects.get(id=questionUser)
        item = Item.objects.get(id=item_id)

        Question.objects.create(
            userFK=user,
            itemFK=item,
            questionText=userQuestion,
            dateTimeOfQuestion=questionTime,
        )
    return JsonResponse({'Success': 'Created'})


def answer(request: HttpRequest, item_id: int) -> JsonResponse:
    if request.method == 'GET':
        return JsonResponse({
            'sellerAnswers': [
                answer.to_dict()
                for answer in Answer.objects.all()
            ]
        })

    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        questionID = body['questionID']
        sellerAnswer = body['sellerAnswer']
        answerTime = body['answerTime']

        item = Item.objects.get(id=item_id)
        question = Question.objects.get(id=questionID)

        Answer.objects.create(
            questionFK=question,
            answerText=sellerAnswer,
            dateTimeOfAnswer=answerTime,
        )
    return JsonResponse({'items': 'shush'})


def search(request: HttpRequest) -> JsonResponse:
    itemList = []
    data = json.loads(request.body)
    query = data['query']

    items = Item.objects.filter(
        Q(title__contains=query) | Q(description__contains=query))

    for item in items:
        obj = {
            'id': item.id,
            'image': item.pictureOfItem.url,
            'listedUser': item.user.username,
            'title': item.title,
            'startingPrice': item.startingPrice,
        }
        itemList.append(obj)
    return JsonResponse({'items': itemList})
