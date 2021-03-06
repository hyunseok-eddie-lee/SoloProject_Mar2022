from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.item import Item
from flask_app.models.user import User


@app.route('/new/item')
def new_item():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": session['user_id']
    }
    return render_template('new_item.html', user=User.get_by_id(data))

@app.route('/create/item', methods=['POST'])
def create_item():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Item.validate_item(request.form):
        return redirect('/new/item')
    data ={
        "clothing_top": request.form["clothing_top"],
        "clothing_bottom": request.form["clothing_bottom"],
        "underwear_swim": request.form["underwear_swim"],
        "pajamas": request.form["pajamas"],
        "shoes_socks": request.form["shoes_socks"],
        "accessory": request.form["accessory"],
        "buying_date": request.form["buying_date"],
        "item_image_url": request.form["item_image_url"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Item.save(data)
    return redirect('/dashboard')

@app.route('/edit/item/<int:id>')
def edit_item(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": id
    }
    user_data ={
        "id": session['user_id']
    }
    return render_template("edit_item.html", edit=Item.get_one(data), user=User.get_by_id(user_data))

@app.route('/update/item', methods=['POST'])
def update_item():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Item.validate_item(request.form):
        return redirect('/new/item')
    data ={
        "clothing_top": request.form["clothing_top"],
        "clothing_bottom": request.form["clothing_bottom"],
        "underwear_swim": request.form["underwear_swim"],
        "pajamas": request.form["pajamas"],
        "shoes_socks": request.form["shoes_socks"],
        "accessory": request.form["accessory"],
        "buying_date": request.form["buying_date"],
        "item_image_url": request.form["item_image_url"],
        "description": request.form["description"],
        "id": request.form["id"]
    }
    Item.update(data)
    return redirect('/dashboard')

# @app.route('/item/<int:id>')
# def show_item(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data ={
#         "id": id
#     }
#     user_data ={
#         "id": session['user_id']
#     }
#     return render_template("show_item.html", item=Item.get_one(data), user=User.get_by_id(user_data))

@app.route('/destroy/item/<int:id>')
def destroy_item(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": id
    }
    Item.destroy(data)
    return redirect('/dashboard')