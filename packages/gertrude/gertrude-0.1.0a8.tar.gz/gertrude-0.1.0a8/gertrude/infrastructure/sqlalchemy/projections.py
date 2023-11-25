# Gertrude --- GTD done right
# Copyright © 2020-2023 Tanguy Le Carrour <tanguy@bioneland.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import datetime
from typing import Optional

from sqlalchemy import Column, Date, MetaData, String, Table
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from gertrude.application import projectors
from gertrude.domain.task_management import dto, enums, projections, value_objects

METADATA = MetaData()
TASKS = Table(
    "tasks",
    METADATA,
    Column("id", String),
    Column("title", String(value_objects.Title.MAX)),
    Column("description", String(value_objects.Description.MAX)),
    Column("state", String),
    Column("belongs_to", String(value_objects.UserId.MAX)),
    Column("assigned_to", String(value_objects.ProjectId.MAX), default=""),
    Column("delegated_to", String(value_objects.Person.MAX), default=""),
    Column("scheduled_on", Date, default=None),
)


class Tasks(projectors.TaskProjection, projections.Tasks):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def capture(self, id: str, belongs_to: str, title: str, description: str) -> None:
        self.__session.execute(
            TASKS.insert().values(
                id=id,
                title=title,
                description=description,
                state=enums.TaskStates.CAPTURED.value,
                belongs_to=belongs_to,
            )
        )

    def update_state(self, id: str, state: str) -> None:
        self.__session.execute(
            TASKS.update().where(TASKS.c.id == id).values(state=state)
        )

    def assign_to(self, id: str, assigned_to: str) -> None:
        self.__session.execute(
            TASKS.update().where(TASKS.c.id == id).values(assigned_to=assigned_to)
        )

    def delegate_to(self, id: str, delegated_to: str) -> None:
        self.__session.execute(
            TASKS.update()
            .where(TASKS.c.id == id)
            .values(state=enums.TaskStates.DELEGATED.value, delegated_to=delegated_to)
        )

    def reclaim(self, id: str, state: str) -> None:
        self.__session.execute(
            TASKS.update().where(TASKS.c.id == id).values(state=state, delegated_to="")
        )

    def schedule_on(self, id: str, date: datetime.date) -> None:
        self.__session.execute(
            TASKS.update()
            .where(TASKS.c.id == id)
            .values(state=enums.TaskStates.SCHEDULED.value, scheduled_on=date)
        )

    def update(self, id: str, title: str, description: str) -> None:
        self.__session.execute(
            TASKS.update()
            .where(TASKS.c.id == id)
            .values(title=title, description=description)
        )

    def load(self, id: str) -> Optional[dto.Task]:
        stmt = select([TASKS]).where(TASKS.c.id == id)
        result = self.__session.execute(stmt).fetchone()
        if result:
            return dto.Task(
                id=result[TASKS.c.id],
                title=result[TASKS.c.title],
                description=result[TASKS.c.description],
                state=result[TASKS.c.state],
                assigned_to=result[TASKS.c.assigned_to],
                delegated_to=result[TASKS.c.delegated_to],
            )
        return None

    def all(self, /, *, state: str = "", assigned_to: str = "") -> list[dto.Task]:
        # FIXME delay added to wait for the projections to be updated.
        import time

        time.sleep(1)

        stmt = select([TASKS])
        if state:
            stmt = stmt.where(TASKS.c.state == state)
        if assigned_to:
            stmt = stmt.where(TASKS.c.assigned_to == assigned_to)

        return [self.__row_to_task(r) for r in self.__session.execute(stmt).fetchall()]

    def __row_to_task(self, row: Row) -> dto.Task:
        return dto.Task(
            id=row[TASKS.c.id],
            title=row[TASKS.c.title],
            description=row[TASKS.c.description],
            state=row[TASKS.c.state],
            delegated_to=row[TASKS.c.delegated_to],
            assigned_to=row[TASKS.c.assigned_to],
        )

    def due(self, date: datetime.date) -> list[dto.Task]:
        # FIXME delay added to wait for the projections to be updated.
        import time

        time.sleep(1)

        stmt = (
            select([TASKS])
            .where(TASKS.c.state == enums.TaskStates.SCHEDULED.value)
            .where(TASKS.c.scheduled_on <= date)
        )
        return [self.__row_to_task(r) for r in self.__session.execute(stmt).fetchall()]
