<template> 
    <div class="dropdown-menu notifications-list" role="menu">
        <div class="notification-list-header">
            <div class="header-items">
                <ul class="notification-item-tabs nav nav-tabs" role="tablist">
                    <li class="notifications-category active" id="notifications" data-toggle="collapse">
                        Notifications
                    </li>
                </ul>
            </div>
        </div>
        <div class="notification-list-body" v-for="notification in notifications">
            <div class="panel-notifications">
                <a class="recent-item notification-item" :href="`/frappedesk/tickets/${notification.document_name && notification.document_name }`">
                    <div class="notification-body">
                        <span class="avatar avatar-medium user-avatar" title="Administrator">
                            <div class="avatar-frame standard-image" style="background-color: #EAF5EE; color: #2F9D58">
                                    {{notification.from_user.slice(0,1)}}
                            </div>
                        </span>
                        <div class="message">
                            <div v-html="notification.subject" />
                            <div class="notification-timestamp text-muted">
                                <span class="frappe-timestamp " data-timestamp="{{ notification.creation }}"> {{ notification.diffDays}} days ago</span>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
        </div>
    </div>
</template>

<style>
.notifications-list .notification-item-tabs {
    border: none;
}
.notifications-list .notification-item-tabs .notifications-category.active {
    color: #1F272E;
    border-bottom: 1px solid #2490EF;
    font-size: 13px;
}
.notifications-list .notification-item-tabs .notifications-category {
    padding: 15px 0px;
    margin-bottom: -1px;
    margin-right: 20px;
    font-weight: 500;
    cursor: pointer;
}
.recent-item:first-child {
    margin-top: 10px;
}
.dropdown-menu a {
    transition: none;
    cursor: pointer;
}
.recent-item {
    padding: 10px;
    margin: 4px 0px;
    border-radius: var(--border-radius-md, 8px);
    white-space: normal;
    font-weight: normal;
    display: flex;
    font-size: small;
    line-height: 20px;
    color: var(--text-light);
    max-width: 455px;
}
.message {
    font-size: 13px;
    font-weight: normal;
}
.recent-item.notification-item .user-avatar .avatar-frame {
    height: 36px;
    width: 36px;
}
.avatar .standard-image {
    border-radius: 50%;
    border: none;
    font-size: 14px;
}
.recent-item.notification-item .notification-body {
    display: flex;
}
.recent-item.notification-item .user-avatar {
    margin-right: 10px;
}
.avatar-medium {
    width: 36px;
    height: 36px;
}
.standard-image {
    object-fit: cover;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: normal;
}
.avatar-frame {
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
}
.recent-item.notification-item .notification-body .message {
    max-width: 360px;
}
.avatar {
    display: inline-block;
    vertical-align: middle;
}
.recent-item.notification-item {
    padding: 10px 10px 10px 4px;
    justify-content: space-between;
}
.panel-notifications {
    width: 100%;
}
.notification-list-body {
    max-height: 500px;
    overflow-y: auto;
}
.notification-list-header {
    margin: 0px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
}
.dropdown-menu {
    z-index: 1000;
    display: block;
    min-width: 200px;
    margin: 1.25rem 0 0;
    color: #1F272E;
    text-align: left;
    list-style: none;
    background-color: #fff;
    -webkit-background-clip: padding-box;
            background-clip: padding-box;
    border-radius: 0.375rem;
    -webkit-box-shadow: 0 6px 12px rgba(0, 0, 0, .175);
            box-shadow: 0 6px 12px rgba(0, 0, 0, .175);
    max-height: 500px;
    overflow: auto;
    font-size: 13px;
    float: none;
    position: absolute;
    }
.notifications-list {
    width: 450px;
    padding: 0px 10px;
    min-height: 560px;
    border: none;
    position: absolute;
    box-shadow: 0px 1px 4px rgba(17, 43, 66, 0.1), 0px 2px 6px rgba(17, 43, 66, 0.08);
}
.notifications-list .notification-list-header {
    margin: 0px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #F4F5F6;
}
.nav {
    display: flex;
    flex-wrap: wrap;
    padding-left: 0;
    margin-bottom: 0;
    list-style: none;
}
</style>

<script>
    
import { inject } from 'vue'

export default {
    name: 'NotificationBox',
    components: {
    },
    data() {
        return {
            notifications: [],
        }
    },
    setup() {
        const user = inject('user')
        return { 
            user
        }
    },
    methods: {
        getDateDiff(date) {
            const currentDate = new Date()
            const creationDate = new Date(date);
            const diffTime = Math.abs(currentDate - creationDate);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
            return diffDays
        }
    },
    resources: {
        notifications() {
            return {
                method: 'frappe.client.get_list',
                params: {
                    doctype: 'Notification Log',
                    fields: ['*'],
                    order_by: 'creation desc',
                },
                auto: true,
                onSuccess: (data) => {
                    if (data){
                        data.forEach(notif => {
                            const diffDays = this.getDateDiff(notif.creation.split(" ")[0])
                            notif["diffDays"] = diffDays
                            this.notifications.push(notif)
                        })
                    }
                }
            }
        },
    },
}
</script>
