import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { GameBoard, Circle } from '../models/game-board.model';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent {
  selectedFile: File | null = null;

  constructor(private router: Router) {}

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  onUpload(): void {
    if (this.selectedFile) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        const fileContent = e.target.result;
        const gameBoard = this.parseFileContent(fileContent);
        localStorage.setItem('gameBoard', JSON.stringify(gameBoard));
        this.router.navigate(['/game-board']);
      };
      reader.readAsText(this.selectedFile);
    }
  }

  parseFileContent(content: string): GameBoard {
    const lines = content.split('\n');
    const size = parseInt(lines[0].trim());
    const circles: Circle[] = [];
    for (let i = 1; i < lines.length; i++) {
      const [row, col, circleType] = lines[i].trim().split(',').map(Number);
      if (!isNaN(row) && !isNaN(col) && !isNaN(circleType)) {
        circles.push({
          x: col,
          y: row,
          color: circleType === 1 ? 'W' : 'B'
        });
      }
    }
    return { size, circles, lines: [] };
  }
}
