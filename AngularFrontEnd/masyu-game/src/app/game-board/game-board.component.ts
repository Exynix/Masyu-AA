import { Component, OnInit } from '@angular/core';
import { GameBoard } from '../models/game-board.model';

@Component({
  selector: 'app-game-board',
  templateUrl: './game-board.component.html',
  styleUrls: ['./game-board.component.css']
})
export class GameBoardComponent implements OnInit {
  gameBoard: GameBoard | null = null;

  ngOnInit(): void {
    const storedGameBoard = localStorage.getItem('gameBoard');
    if (storedGameBoard) {
      this.gameBoard = JSON.parse(storedGameBoard);
    }
  }

  getCircleClass(x: number, y: number): string {
    if (!this.gameBoard) return '';
    const circle = this.gameBoard.circles.find(c => c.x === x && c.y === y);
    if (circle) {
      return circle.color === 'B' ? 'circle-b' : 'circle-w';
    }
    return '';
  }
}
