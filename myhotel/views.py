import datetime
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from myhotel.models import Customer, User, bill, collection, items

# Create your views here.
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    table_count=21
    customer_data_list = []
    for a in range(1,31):
        try:
            customer_data = Customer.objects.get(hotel_id=request.session.get('user_id'), table_no=a)
            customer_name=customer_data.customer_name
        except:
            customer_data=None
            customer_name=None
        try:
            billing_data=bill.objects.filter(hotel_id=request.session.get('user_id'),table_no=a)
            Total=0
            for b in billing_data:
                Total=Total+b.Total
        except:
            billing_data=None
            Total=None
        customer_data_list.append({'table_no':a,'customer_name': customer_name, 'total': Total})


    return render(request,'dashboard.html' ,{'customer_data_list':customer_data_list})

















def make_bill(request,table_id):
    if 'user_id' not in request.session:
        return redirect('/')
    dish_data=items.objects.filter(hotel_id=request.session.get('user_id'))
    billing_data=bill.objects.filter(hotel_id=request.session.get('user_id'),table_no=table_id)
    Total_Count=0
    for bills_total in billing_data:
        Total_Count=Total_Count+bills_total.Total
    try:
        customer_data = Customer.objects.get(hotel_id=request.session.get('user_id'), table_no=table_id)
    except:
        customer_data=None

    customer_info_data = []
    for table_number_idx in range(1, 31):
        try:
            customer_info_obj = Customer.objects.get(hotel_id=request.session.get('user_id'), table_no=table_number_idx)
            customer_name_val = customer_info_obj.customer_name
        except Customer.DoesNotExist:
            customer_info_obj = None
            customer_name_val = None
        
        try:
            billing_info_set = bill.objects.filter(hotel_id=request.session.get('user_id'), table_no=table_number_idx)
            total_val = 0
            for bill_info in billing_info_set:
                total_val += bill_info.Total
        except bill.DoesNotExist:
            billing_info_set = None
            total_val = None
        
        customer_info_data.append({'table_number_idx': table_number_idx, 'customer_name_val': customer_name_val, 'total_amount_val': total_val})

    return render(request,'makebill.html' ,{'customer_data_list':customer_info_data,'customer_data':customer_data,'Total_Count':Total_Count,'table_id':table_id,'dish_data':dish_data,'billing_data':billing_data})

def save_bill(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        # Get form data
        try:
            hotel_id = request.session.get('user_id')
            table_no = int(request.POST.get('table_no'))
            item_name = request.POST.get('dishName')
            print(item_name)
            quantity_str = request.POST.get('quantity')
            unit_price_str = request.POST.get('unitPrice')
            # print(quantity_str,unit_price_str)
            if quantity_str and unit_price_str:
                quantity = float(quantity_str)
                unit_price = float(unit_price_str)
                total = unit_price * quantity  # Calculate total

                # Create a new instance of the bill model
                new_bill = bill.objects.create(
                    hotel_id=hotel_id,
                    table_no=table_no,
                    Item_Name=item_name,
                    unit_Price=unit_price,
                    quantity=quantity,
                    Total=total
                )
                # Optionally, you can save the instance to the database
                new_bill.save()

                # Redirect to a success page or render another template
                # messages.success(request, "Item Added In Bill successfully!")
                return redirect(f'/myhotel/makebill/{table_no}')  # Redirect with the same table_no
            else:
                # Handle empty quantity or unit price
                messages.error(request, "Quantity or Unit Price cannot be empty!")
                return redirect(f'/myhotel/makebill/{table_no}')  # Redirect with the same table_no
            
        except Exception as e:
            print(e)
            messages.error(request, "Oops! Something Went Wrong!")
            return redirect(f'/myhotel/makebill/{table_no}')  # Redirect with the same table_no
    else:
        # Handle other request methods here, if necessary
        messages.error(request, "Oops! Something went Wrong!")
        pass
def delete_bill_item(request, pk, table_id):
    if 'user_id' not in request.session:
        return redirect('/')
    try:
        deleteme=bill.objects.get(pk=pk)
        deleteme.delete()
        # messages.error(request,f"{deleteme.Item_Name} Remove From Bill Successfully!")
    except:
        messages.error(request,"Oops! Something Wrong!")

    return redirect(f'/myhotel/makebill/{table_id}')  # Redirect with the same table_no
def cust_details(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        # Get form data
        try:
            hotel_id = request.session.get('user_id')
            table_no = int(request.POST.get('cust_table_id'))
            customerName = request.POST.get('customerName')
            customerMobile = request.POST.get('customerMobile')
            try:
                customer_data = Customer.objects.get(hotel_id=hotel_id, table_no=table_no)
            except Customer.DoesNotExist:
                # If customer data doesn't exist, create a new instance
                customer_data = Customer(hotel_id=hotel_id, table_no=table_no)

            # Update customer data with the new values
            customer_data.customer_name = customerName
            customer_data.customer_mobile_number = customerMobile

            # Save the customer data
            customer_data.save()
            # messages.success(request,"Customer Name Added Successfully!")

        except:
            messages.error(request,"Oops! Something Wrong!")

    return redirect(f'/myhotel/makebill/{table_no}')  # Redirect with the same table_no
def delete_bill(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        # Get form data
        try:
            hotel_id = request.session.get('user_id')
            table_no = int(request.POST.get('table_no_delete'))
            try:
                try:
                    customer_data = Customer.objects.get(hotel_id=hotel_id, table_no=table_no)
                    customer_data.delete()
                except:
                    pass
                customer_data = bill.objects.filter(hotel_id=hotel_id, table_no=table_no)
                customer_data.delete()

                # messages.success(request,"Record Deleted Successfully!")
            except:
                messages.error(request,"Oops! Something went Wrong!")
                pass
        except:
            messages.error(request,"Oops! Something Wrong!")

    return redirect(f'/myhotel/makebill/{table_no}')  # Redirect with the same table_no










def generate(request,table_id):
    if 'user_id' not in request.session:
        return redirect('/')
    

    cllection_model=collection()
    try:
        customer_data = Customer.objects.get(hotel_id=request.session.get('user_id'), table_no=table_id)
        cllection_model.Customer_name=customer_data.customer_name
        cllection_model.mobile=customer_data.customer_mobile_number
    except:
        pass
    try:
        customer_data = bill.objects.filter(hotel_id=request.session.get('user_id'), table_no=table_id)
        if customer_data:
            Total=0
            for a in customer_data:
                Total=Total+a.Total
            cllection_model.Total=Total
            cllection_model.hotel_id=request.session.get('user_id')
            cllection_model.table_no=table_id
            cllection_model.date=datetime.date.today()
            cllection_model.save()
    except Exception as e:
        print(e)
        pass


    billing_data=bill.objects.filter(hotel_id=request.session.get('user_id'),table_no=table_id)
    Total_Count=0
    for bills_total in billing_data:
        Total_Count=Total_Count+bills_total.Total
    try:
        customer_data = Customer.objects.get(hotel_id=request.session.get('user_id'), table_no=table_id)
    except:
        customer_data=None
    hotel_name=request.session.get('hotel')
    contact1=request.session.get('contact1')
    contact2=request.session.get('contact2')
    address=User.objects.get(pk=request.session.get('user_id'))
    address=address.address
    return render(request,'generate.html' ,{'address':address,'hotel_name':hotel_name,'contact1':contact1,'contact2':contact2,'Total_Count':Total_Count,'billing_data':billing_data,'table_id':table_id,'customer_data':customer_data})




def item_details(request):
        if 'user_id' in request.session:
            
            if request.method == 'POST':
                item=items()
                item.Item_Name = request.POST.get("Item_Name").strip()
                item.unit_Price = request.POST.get("unit_price").strip()
                Item_Name=request.POST.get("Item_Name").strip()
                user_id = request.session.get('user_id')
                item.hotel_id=user_id


            
                try:
                    # Check if an item with the given Item_Name and Store_id exists
                    item_check = items.objects.filter(Item_Name=Item_Name, hotel_id=user_id)

                    if item_check.exists():
                        messages.error(request, "Item Not Added! The Item Is Already Added")
                    else:
                        item.save()
                        # messages.success(request, "Item Added successfully!")
                except Exception as e:
                    print(e)
                    messages.error(request, "Item Not Added!")
            user_id = request.session.get('user_id')
            item = items.objects.filter(hotel_id=user_id)
            user_id = request.session.get('user_id')
            return render(request,"items.html",{
                 'item': item})

        else:
            # User is not logged in, redirect to the login page
            return redirect('/')  # Replace '/login/' with the actual URL for your login page
        
    


    
def update_item(request, item_id):
        if 'user_id' in request.session:
            if request.method == 'POST':
                user_id = request.session.get('user_id')
                item = items.objects.get(pk=item_id, hotel_id=user_id)
                item.Item_Name = request.POST.get("Item_Name").strip()
                item.unit_Price = request.POST.get("Price_For_Cash_Cust").strip()
            
                try:
                    item.save()
                    # messages.success(request, "Item updated successfully!")
                    return redirect('/myhotel/item/')
                except:
                    messages.error(request, "Item Not updated!")
                    return redirect('/myhotel/item/')
            else:
                messages.error(request, "Something wents to wrong!!!")
    
        else:
            # User is not logged in, redirect to the login page
            return redirect('/')  # Replace '/login/' with the actual URL for your login page
        
        
    

def delete_item(request, item_id):
        if 'user_id' in request.session:
            user_id = request.session.get('user_id')
            item = items.objects.get(pk=item_id, hotel_id=user_id)
            try:
                item.delete()
                # messages.success(request, "Item Deleted successfully!")
                return redirect('/myhotel/item/')
            except:
                messages.error(request, "Item Not Deleted!")
                return redirect('/myhotel/item/')

        else:
            # User is not logged in, redirect to the login page
            return redirect('/')  # Replace '/login/' with the actual URL for your login page

def collections(request):
        if 'user_id' in request.session:
            user_id = request.session.get('user_id')
            collection_model = collection.objects.filter(hotel_id=user_id)
            return render(request,"collection.html",{"collection_model":collection_model})
        else:
            # User is not logged in, redirect to the login page
            return redirect('/')  # Replace '/login/' with the actual URL for your login page
        
   
