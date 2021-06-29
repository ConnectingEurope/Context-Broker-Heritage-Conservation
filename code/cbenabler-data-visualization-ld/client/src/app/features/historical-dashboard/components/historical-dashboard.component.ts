import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-historical-dashboard',
  templateUrl: './historical-dashboard.component.html',
  styleUrls: ['./historical-dashboard.component.scss'],
})
export class HistoricalDashboardComponent implements OnInit {

  public dailyDashboard: any = "http://your_ip/app/dashboards#/"; // // Copy here the dashboard URL from your Kibana
  public monthlyDashboard: any = "http://your_ip/app/dashboards#/"; // // Copy here the dashboard URL from your Kibana
  public annualDashboard: any = "http://your_ip/app/dashboards#/"; // // Copy here the dashboard URL from your Kibana
  public exteriorDashboard: any = "http://your_ip/app/dashboards#/"; // // Copy here the dashboard URL from your Kibana
  public dashboardRef: any;
  public currentDashboard: string = "Daily";
  constructor(private sanitizer: DomSanitizer) {
    this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.dailyDashboard);
   }


  public ngOnInit(): void {
  }
  public changeDashboard(dashboard: string): void {
    switch (dashboard) {
      case 'exterior':
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.exteriorDashboard);
        this.currentDashboard = "Exterior";
        break;
      case 'daily':
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.dailyDashboard);
        this.currentDashboard = "Daily";
        break;
      case 'monthly':
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.monthlyDashboard);
        this.currentDashboard = "Monthly";
        break;
      case 'annual':
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.annualDashboard);
        this.currentDashboard = "Annual";
        break;
    }
  }

}

