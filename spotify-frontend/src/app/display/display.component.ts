import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-display',
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.css']
})
export class DisplayComponent {
  @Input() record: any
  dataSource : any
  displayedColumns: string[] = ['AlbumName', 'ArtistName', 'SpotifyUrl', 'TrackName'];
}
