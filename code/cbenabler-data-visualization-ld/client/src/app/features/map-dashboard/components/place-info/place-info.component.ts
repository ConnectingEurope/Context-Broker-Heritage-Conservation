import { Component, Input, OnInit } from '@angular/core';
import { Entity } from 'src/app/shared/models/entity';
import { ModelDto } from 'src/app/shared/models/model-dto';
import { MapDashboardService } from '../../services/map-dashboard.service';

@Component({
  selector: 'app-place-info',
  templateUrl: './place-info.component.html',
  styleUrls: ['./place-info.component.scss'],
})
export class PlaceInfoComponent implements OnInit {

  private firstLoad: boolean = false;
  buildingEntity: Entity;
  capilleEntity: Entity;
  centralEntity: Entity;
  airQualityEntity: Entity;

  constructor( private mapDashBoardService: MapDashboardService) {

    this.mapDashBoardService.getEntitiesData(!this.firstLoad).toPromise().then(
      (models: ModelDto[]) => {
        models.forEach((model, i) => {
          model.data.forEach(entity =>{
             switch(entity.id){
              case 'urn:ngsi-ld:AirQualityObserved:Sevilla:AQO001':
                this.airQualityEntity = entity;
                break;
              case 'urn:ngsi-ld:Building:Sevilla:Nave-central---Iglesia-San-Luis-de-los-Franceses:B001':
                this.buildingEntity = entity;
                break;
              case 'urn:ngsi-ld:IndoorEnvironmentObserved:Sevilla:Nave-central---Iglesia-San-Luis-de-los-Franceses:IE006':
                this.centralEntity = entity;
                break;
              case 'urn:ngsi-ld:IndoorEnvironmentObserved:Sevilla:Capilla---Iglesia-San-Luis-de-los-Franceses:IE005':
                this.capilleEntity = entity;
                break;    
             }
          });
         
      });
      });
   }

  public ngOnInit(): void {

  }

}
