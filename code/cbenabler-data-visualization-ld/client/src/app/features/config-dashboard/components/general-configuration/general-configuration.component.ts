import { Component, Input, OnDestroy, ViewChild, Output, EventEmitter } from '@angular/core';
import { ConfigDashboardService } from '../../services/config-dashboard.service';
import { takeUntil } from 'rxjs/operators';
import { BaseComponent } from 'src/app/shared/misc/base.component';
import { ContextBrokerForm } from '../../models/context-broker-form';
import { InputWithValidationComponent } from 'src/app/shared/templates/input-with-validation/input-with-validation.component';
import { TreeNode } from 'primeng/api/treenode';
import { SubscriptionsDialogComponent, ContextSubscription } from '../subscriptions-dialog/subscriptions-dialog.component';
import { EntityTreeNodeService } from '../../services/entity-tree-node.service';
import { TreeNodeService } from 'src/app/shared/services/tree-node.service';
import { TypeContainerDto } from '../../models/type-container-dto';

@Component({
    selector: 'app-general-configuration',
    templateUrl: './general-configuration.component.html',
    styleUrls: ['./general-configuration.component.scss'],
})
export class GeneralConfigurationComponent extends BaseComponent implements OnDestroy {

    @Input() public cb: ContextBrokerForm;
    @Output() public selectedEntitiesChange: EventEmitter<void> = new EventEmitter<void>();
    @Output() public favChange: EventEmitter<void> = new EventEmitter<void>();
    @Output() public urlChange: EventEmitter<void> = new EventEmitter<void>();

    public chooseWarningVisible: boolean;
    public subsWarningVisible: boolean;
    public displaySubs: boolean;
    public displaySubsContent: ContextSubscription[];

    @ViewChild('urlInput') private urlInput: InputWithValidationComponent;
    @ViewChild('subscriptionDialog') private subscriptionDialog: SubscriptionsDialogComponent;

    constructor(
        private configDashboardService: ConfigDashboardService,
        private treeNodeService: TreeNodeService,
        private entityTreeNodeService: EntityTreeNodeService,
    ) {
        super();
    }

    /*****************************************************************************
     Event functions
    *****************************************************************************/

    public onNameChange(): void {
        const header: string = this.cb.form.value.name;
        this.cb.header = header && !/^\s+$/.test(header) ? header : this.configDashboardService.contextHeaderWhenEmpty;
    }

    public onUrlChange(): void {
        this.chooseWarningVisible = false;
        this.subsWarningVisible = false;
        this.urlChange.emit();
    }

    public onSelectedEntitiesChange(selectedEntities: TreeNode[]): void {
        this.cb.selectedEntities = selectedEntities;
        this.selectedEntitiesChange.emit();
    }

    public onFavChange(): void {
        this.favChange.emit();
    }

    public onCheckContextBroker(): void {
        const url: string = this.cb.form.value.url;

        this.configDashboardService.checkBrokerHealth(url).pipe(takeUntil(this.destroy$)).subscribe(
            isLive => {
                isLive ? this.onCheckContextBrokerSuccess() : this.onCheckContextBrokerFail(isLive);

            },
            err => {
                this.onCheckContextBrokerFail(err);
            });
    }

    public onChooseEntities(): void {
        const url: string = this.cb.form.value.url;

        this.configDashboardService.getEntitiesFromService(url).pipe(takeUntil(this.destroy$)).subscribe(
            types => {
                types.length > 0 ? this.onChooseEntitiesSuccess(types) : this.onChooseEntitiesFail();
            },
            err => {
                this.onChooseEntitiesFail();
            });
    }

    public onClickSubscriptions(): void {
        this.configDashboardService.getSubscriptions(this.cb.form.get('url').value).pipe(takeUntil(this.destroy$)).subscribe(
            subs => {
                if (subs.length > 0) {
                    this.onClickSubscriptionsSuccess(subs);
                } else {
                    this.onClickSubscriptionsFail();
                }
            },
            err => {
                this.onClickSubscriptionsFail();
            },
        );
    }

    /*****************************************************************************
     Button visibility functions
    *****************************************************************************/

    public shouldChooseButtonBeDisabled(): boolean {
        return this.cb.form.get('url').invalid;
    }

    public shouldSubsButtonBeDisabled(): boolean {
        return this.shouldChooseButtonBeDisabled();
    }

    /*****************************************************************************
     Check Context Broker functions
    *****************************************************************************/

    private onCheckContextBrokerSuccess(): void {
        this.urlInput.showInfo();
    }

    private onCheckContextBrokerFail(err: boolean): void {

        this.urlInput.showWarning();
    }

    /*****************************************************************************
     Choose entities functions
    *****************************************************************************/

    private onChooseEntitiesSuccess(types: TypeContainerDto[]): void {
        this.chooseWarningVisible = false;
        this.cb.entities = this.entityTreeNodeService.convertEntitiesToNodes(types);
        this.cb.selectedEntities = this.treeNodeService.getAllSelected(this.cb.entities);
        this.selectedEntitiesChange.emit();
    }

    private onChooseEntitiesFail(): void {
        this.chooseWarningVisible = true;
        this.cb.entities = [];
        this.cb.selectedEntities = [];
    }

    /*****************************************************************************
     Subscriptions functions
    *****************************************************************************/

    private onClickSubscriptionsSuccess(subs: ContextSubscription[]): void {
        this.subsWarningVisible = false;
        this.subscriptionDialog.updateContent(subs);
        this.displaySubs = true;
    }

    private onClickSubscriptionsFail(): void {
        this.subsWarningVisible = true;
    }

}
