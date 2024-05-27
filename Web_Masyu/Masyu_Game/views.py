from django.shortcuts import render
from django.http import HttpResponse
from .models import GameBoard
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# Create your views here.
def upload_file(request):
    if request.method == 'POST' and request.FILES['board_file']:
        board_file = request.FILES['board_file']
        fs = FileSystemStorage()
        filename = fs.save(board_file.name, board_file)
        file_path = fs.path(filename)
        game_board = GameBoard.load_from_file(file_path)
        return redirect('game_board_view', board_id=game_board.id)
    return render(request, 'Masyu_Game/upload_file.html')

def game_board_view(request, board_id):
    game_board = GameBoard.objects.get(id=board_id)
    size_range = range(game_board.size)
    board = [[None for _ in size_range] for _ in size_range]

    for circle in game_board.circles.all():
        board[circle.y - 1][circle.x - 1] = circle.color.lower()

    return render(request, 'Masyu_Game/game_board.html', {'game_board': game_board, 'size_range': size_range, 'board': board})