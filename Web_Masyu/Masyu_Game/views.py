from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import GameBoard, Circle, Line

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
    board_dict = {}

    for circle in game_board.circles.all():
        print(f"Circle at ({circle.x}, {circle.y}) is {circle.color}")
        board_dict[(circle.y - 1, circle.x - 1)] = circle.color.lower()

    return render(request, 'Masyu_Game/game_board.html', {'game_board': game_board, 'size_range': size_range, 'board': board_dict})


def add_line(request):
    if request.method == 'POST':
        x1 = int(request.POST['x1'])
        y1 = int(request.POST['y1'])
        x2 = int(request.POST['x2'])
        y2 = int(request.POST['y2'])
        board_id = int(request.POST['board_id'])

        game_board = GameBoard.objects.get(id=board_id)

        # Check if the line is valid (adjacent cells)
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return JsonResponse({'status': 'failed', 'error': 'Lines must connect adjacent cells.'})

        line = Line.objects.create(x1=x1, y1=y1, x2=x2, y2=y2)
        game_board.lines.add(line)

        # TODO: Add validation logic to check game rules

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})


