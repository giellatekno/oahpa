

def dialect(request):
    return {'dialect': request.session.get('dialect')}

