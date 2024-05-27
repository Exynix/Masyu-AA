

export interface GameBoard {
  size: number;
  circles: Circle[];
  lines: Line[];
}


export interface Circle {
  color: 'B' | 'W';
  x: number;
  y: number;
}

export interface Line {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}
