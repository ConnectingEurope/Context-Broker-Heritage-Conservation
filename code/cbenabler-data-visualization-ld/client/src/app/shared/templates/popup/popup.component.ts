import { Component, Input, ViewChild, Output, EventEmitter } from '@angular/core';
import * as moment from 'moment';
import { ScrollPanel } from 'primeng/scrollpanel/public_api';
import { Router } from '@angular/router';
import { ModelDto } from '../../models/model-dto';
import { EntityMetadataService } from '../../services/entity-metadata-service';
import { BaseComponent } from '../../misc/base.component';
import { takeUntil } from 'rxjs/operators';
import { Entity } from '../../models/entity';

@Component({
    selector: 'app-popup',
    templateUrl: './popup.component.html',
    styleUrls: ['./popup.component.scss'],
})
export class PopupComponent extends BaseComponent {

    @Input() public entity: Entity;
    @Input() public modelDto: ModelDto;
    @Output() public clickDebug: EventEmitter<void> = new EventEmitter<void>();

    public maxNumberAttrsUntilScroll: number = 10;
    public attrs: any[];

    private maxNumberChars: number = 30;

    @ViewChild('scrollPanel') private scrollPanel: ScrollPanel;

    constructor(
        private router: Router,
        private entityMetadataService: EntityMetadataService,
    ) {
        super();
    }

    public updatePopup(entity: any, modelDto: ModelDto): void {
        this.entity = entity;
        this.modelDto = modelDto;
        this.updateAttrs();
    }

    public refreshScroll(): void {
        if (this.scrollPanel) {
            this.scrollPanel.refresh();
        }
    }

    public onClickStats(): void {
        this.entityMetadataService.setEntityMetadata(this.entity, this.modelDto).pipe(takeUntil(this.destroy$)).subscribe(() => {
            this.router.navigate(['/historical-data', this.modelDto.type, this.entity.id]);
        });
    }

    public onClickDebug(): void {
        this.clickDebug.emit();
    }

    private updateAttrs(): void {
        this.attrs = Object.entries(this.entity).filter(a => a[0] !== 'location').map(a => [this.transformKey(a[0]), this.transformAttr(a[0], a[1])]);
    }

    private transformKey(key:string){
        let transformedKey;
        switch(key){
        case 'description':
            transformedKey = 'Description';
            break;
        case 'dateObserved':
            transformedKey = 'Date observed';
            break;
        case 'dataProvider':
            transformedKey = 'Data provider';
            break;
        case 'relativeHumidity':
            transformedKey = "Relative humidity";
            break;
        case 'atmosphericPressure':
            transformedKey = "Atmospheric pressure";
            break;
        case 'co2Level':
            transformedKey = "CO2 Level";
            break;
        case 'tvocLevel':
            transformedKey = "TVOC Level";
            break;
        case 'temperature':
            transformedKey = "Temperature";
            break;
        case 'illuminance':
            transformedKey = "Illuminance";
            break;
        case 'infrared':
            transformedKey = "Infrared";
            break;
        case 'co2':
            transformedKey = "CO2";
            break;
        case 'tvoc':
            transformedKey = "TVOC";
            break;
        case 'type':
            transformedKey = "Type";
            break;
        case 'name':
            transformedKey = "Name";
            break;
        case 'id':
            transformedKey = 'Id';
            break;
        case 'peopleOccupancy':
            transformedKey = 'People Occupancy';
            break;
        case 'peopleCapacity':
            transformedKey = 'People Occupancy';
            break;
        case 'category':
            transformedKey = "Category";
            break;
        case 'address':
            transformedKey = 'Address';
            break;
        case 'openingHours':
            transformedKey = 'Opening Hours';
            break;
        case 'source':
            transformedKey = 'Source';
            break;
        case 'dateIssued':
            transformedKey = 'Date Issued';
            break;
        case 'dayMinimum':
            transformedKey = 'Day minimum';
            break;
        case 'dayMaximum':
            transformedKey = 'Day maximum';
            break;
        case 'feelsLikeTemperature':
            transformedKey = 'Feels like temperature';
            break;
        case 'weatherType':
            transformedKey = 'Weather type';
            break;
        case 'precipitationProbability':
            transformedKey = 'Precipitation probability';
            break;
        case 'windSpeed':
            transformedKey = 'Wind speed';
            break;
        case 'uvIndexMax':
            transformedKey = 'UV index max';
            break;
        case 'typeOfLocation':
            transformedKey = 'Type of locatiobn';
            break;
        case 'airQualityIndex':
            transformedKey = 'Air quality index(AQI)';
            break;
        case 'airQualityLevel':
            transformedKey = 'Air quality level';
            break;
        case 'co':
            transformedKey = 'CO';
            break;
        case 'so2':
            transformedKey = 'SO2';
            break;
        case 'no2':
            transformedKey = 'NO2';
            break; 
        case 'o3':
            transformedKey = 'O3';
            break; 
        case 'no2':
            transformedKey = 'NO2';
            break; 
        default:
            transformedKey = key;
        }
        return transformedKey;
    }
    private transformAttr(key: string, value: any): any {
        let v: any = value;
        const dateExp: RegExp = new RegExp(/.*-.*-.*:.*:.*\..*Z/);

        if (dateExp.test(v)) { return moment(v).format('DD/MM/YYYY HH:mm:ss'); }
        if (typeof v === 'object') { return v = JSON.stringify(v); }
        return value;
    }

}
