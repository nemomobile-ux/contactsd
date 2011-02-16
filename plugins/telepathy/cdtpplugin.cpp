/***************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (people-users@projects.maemo.org)
**
** This file is part of contactsd.
**
** If you have questions regarding the use of this file, please contact
** Nokia at people-users@projects.maemo.org.
**
** This library is free software; you can redistribute it and/or
** modify it under the terms of the GNU Lesser General Public
** License version 2.1 as published by the Free Software Foundation
** and appearing in the file LICENSE.LGPL included in the packaging
** of this file.
**
****************************************************************************/

#include "cdtpplugin.h"

#include "cdtpcontroller.h"

#include <TelepathyQt4/Debug>

CDTpPlugin::CDTpPlugin()
    : mController(0)
{
}

CDTpPlugin::~CDTpPlugin()
{
}

void CDTpPlugin::init()
{
    qDebug() << "Initializing contactsd telepathy plugin";

    Tp::registerTypes();
    Tp::enableDebug(true);
    Tp::enableWarnings(true);

    qDebug() << "Creating controller";
    mController = new CDTpController(this);
    // relay signals
    connect(mController,
            SIGNAL(importStarted(const QString &, const QString &)),
            SIGNAL(importStarted(const QString &, const QString &)));
    connect(mController,
            SIGNAL(importEnded(const QString &, const QString &, int, int, int)),
            SIGNAL(importEnded(const QString &, const QString &, int, int, int)));
}

QMap<QString, QVariant> CDTpPlugin::metaData()
{
    QMap<QString, QVariant> data;
    data[CONTACTSD_PLUGIN_NAME]    = QVariant(QString::fromLatin1("telepathy"));
    data[CONTACTSD_PLUGIN_VERSION] = QVariant(QString::fromLatin1("0.1"));
    data[CONTACTSD_PLUGIN_COMMENT] = QVariant(QString::fromLatin1("contactsd telepathy plugin"));
    return data;
}

Q_EXPORT_PLUGIN2(CDTpPlugin, CDTpPlugin)
