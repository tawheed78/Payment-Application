from django.shortcuts import redirect, render
from .utils import initiate_payment, client
import razorpay
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_gateway = request.POST.get('payment_gateway')
        context = {
            'amount': amount,
            'payment_gateway': payment_gateway
        }
        if payment_gateway == 'Razorpay':
            # payment_view(int(amount))
            return redirect('payment', amount=amount)
    return render(request, 'home.html')     

@csrf_exempt
def payment_view(request):
   amount = int(request.POST.get('amount'))  # Set the amount dynamically or based on your requirements
   order_id = initiate_payment(amount)
   context = {
       'order_id': order_id,
       'amount': amount
   }
   print(context)
   return render(request, 'payment.html', context)

@csrf_exempt
def payment_success_view(request):
   print(request.POST)
   order_id = request.POST.get('order_id')
   payment_id = request.POST.get('razorpay_payment_id')
   signature = request.POST.get('razorpay_signature')
   params_dict = {
       'razorpay_order_id': order_id,
       'razorpay_payment_id': payment_id,
       'razorpay_signature': signature
   }
   print(params_dict)
   try:
       client.utility.verify_payment_signature(params_dict)
       # Payment signature verification successful
       # Perform any required actions (e.g., update the order status)
       return render(request, 'payment_success.html')
   except razorpay.errors.SignatureVerificationError as e:
       # Payment signature verification failed
       # Handle the error accordingly
       return render(request, 'payment_failure.html')