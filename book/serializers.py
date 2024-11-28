def get_book_response(obj):

    response = dict()

    response['book_name'] = obj.name
    response['book_price'] = obj.price
    response['book_is_offer'] = obj.is_offer


    return response