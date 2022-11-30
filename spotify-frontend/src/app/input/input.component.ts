import { Component ,EventEmitter, Output} from '@angular/core';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent { 
  @Output() searchSpotifyDb = new EventEmitter<any>();
  onButtonClick(value:string){
    this.searchSpotifyDb.emit({searchquery:value})
  }
}
