import { Component,OnInit } from '@angular/core';
import {ApiService} from  './api.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'spotify-frontend';
  all_records: Array<any>
  constructor(private api: ApiService) {  
 }
  handleSpotifyDbClick(eventData: { searchquery: string }){
      this.api.getSongdata(eventData.searchquery).subscribe((data : any)=>{
      this.all_records = data.tracks
      console.log(this.all_records)
   });
  }
}
