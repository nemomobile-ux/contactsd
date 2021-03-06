/** This file is part of Contacts daemon
 **
 ** Copyright (c) 2010-2011 Nokia Corporation and/or its subsidiary(-ies).
 **
 ** Contact:  Nokia Corporation (info@qt.nokia.com)
 **
 ** GNU Lesser General Public License Usage
 ** This file may be used under the terms of the GNU Lesser General Public License
 ** version 2.1 as published by the Free Software Foundation and appearing in the
 ** file LICENSE.LGPL included in the packaging of this file.  Please review the
 ** following information to ensure the GNU Lesser General Public License version
 ** 2.1 requirements will be met:
 ** http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
 **
 ** In addition, as a special exception, Nokia gives you certain additional rights.
 ** These rights are described in the Nokia Qt LGPL Exception version 1.1, included
 ** in the file LGPL_EXCEPTION.txt in this package.
 **
 ** Other Usage
 ** Alternatively, this file may be used in accordance with the terms and
 ** conditions contained in a signed written agreement between you and Nokia.
 **/

#ifndef CDBIRTHDAYCONTROLLER_H
#define CDBIRTHDAYCONTROLLER_H

#include "cdbirthdaycalendar.h"

#include <QSet>
#include <QObject>
#include <QTimer>

#include <QContact>
#include <QContactAbstractRequest>
#include <QContactFetchRequest>
#include <QContactManager>

class CDBirthdayCalendar;

QTCONTACTS_USE_NAMESPACE

class CDBirthdayController : public QObject
{
    Q_OBJECT

    enum SyncMode {
        Incremental,
        FullSync
    };

public:
    explicit CDBirthdayController(QObject *parent = 0);
    ~CDBirthdayController();

private Q_SLOTS:
    void contactsChanged(const QList<QContactId> &contacts);
    void contactsRemoved(const QList<QContactId> &contacts);

    void onRequestStateChanged(QContactAbstractRequest::State newState);
    void updateAllBirthdays();
    void onUpdateQueueTimeout();

private:
    static void createStampFile();
    static QString stampFilePath();
    static bool stampFileUpToDate();

    void fetchContacts(const QContactFilter &filter, SyncMode mode);
    void updateBirthdays(const QList<QContact> &changedBirthdays);
    void syncBirthdays(const QList<QContact> &birthdayContacts);

private:
    CDBirthdayCalendar mCalendar;
    QContactManager mManager;
    QScopedPointer<QContactFetchRequest> mRequest;
    QSet<QContactId> mUpdatedContacts;
    QTimer mUpdateTimer;
    SyncMode mSyncMode;
    bool mUpdateAllPending;
};

#endif // CDBIRTHDAYCONTROLLER_H
