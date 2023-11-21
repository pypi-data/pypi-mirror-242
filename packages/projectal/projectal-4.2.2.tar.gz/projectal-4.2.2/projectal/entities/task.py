import datetime

import projectal
from projectal.entity import Entity
from projectal.enums import DateLimit
from projectal.linkers import *


class Task(
    Entity,
    ResourceLinker,
    SkillLinker,
    FileLinker,
    StageLinker,
    StaffLinker,
    RebateLinker,
    NoteLinker,
    TagLinker,
):
    """
    Implementation of the [Task](https://projectal.com/docs/latest/#tag/Task) API.
    """

    _path = "task"
    _name = "task"
    _links = [
        ResourceLinker,
        SkillLinker,
        FileLinker,
        StageLinker,
        StaffLinker,
        RebateLinker,
        NoteLinker,
        TagLinker,
    ]

    @classmethod
    def create(cls, holder, entities):
        """Create a Task

        `holder`: An instance or the `uuId` of the owner

        `entities`: `dict` containing the fields of the entity to be created,
        or a list of such `dict`s to create in bulk.
        """
        holder_id = holder["uuId"] if isinstance(holder, dict) else holder
        params = "?holder=" + holder_id
        out = super().create(entities, params)

        # Tasks should always refer to their parent and project. We don't get this information
        # from the creation api method, but we can insert them ourselves because we know what
        # they are.
        def add_fields(obj):
            obj.set_readonly("projectRef", holder_id)
            obj.set_readonly("parent", obj.get("parent", holder_id))

        if isinstance(out, dict):
            add_fields(out)
        if isinstance(out, list):
            for obj in out:
                add_fields(obj)
        return out

    def update_order(self, order_at_uuId, order_as=True):
        url = "/api/task/update?order-at={}&order-as={}".format(
            order_at_uuId, "true" if order_as else "false"
        )
        return api.put(url, [{"uuId": self["uuId"]}])

    def link_predecessor_task(self, predecessor_task):
        return self.__plan(self, predecessor_task, "add")

    def relink_predecessor_task(self, predecessor_task):
        return self.__plan(self, predecessor_task, "update")

    def unlink_predecessor_task(self, predecessor_task):
        return self.__plan(self, predecessor_task, "delete")

    @classmethod
    def __plan(cls, from_task, to_task, operation):
        url = "/api/task/plan/task/{}".format(operation)
        payload = {"uuId": from_task["uuId"], "taskList": [to_task]}
        api.post(url, payload=payload)
        return True

    def parents(self):
        """
        Return an ordered list of [name, uuId] pairs of this task's parents, up to
        (but not including) the root of the project.
        """
        payload = {
            "name": "Task Parents",
            "type": "msql",
            "start": 0,
            "limit": -1,
            "holder": "{}".format(self["uuId"]),
            "select": [
                ["TASK(one).PARENT_ALL_TASK.name"],
                ["TASK(one).PARENT_ALL_TASK.uuId"],
            ],
        }
        list = api.query(payload)
        # Results come back in reverse order. Flip them around
        list.reverse()
        return list

    def project_uuId(self):
        """Return the `uuId` of the Project that holds this Task."""
        payload = {
            "name": "Project that holds this task",
            "type": "msql",
            "start": 0,
            "limit": 1,
            "holder": "{}".format(self["uuId"]),
            "select": [["TASK.PROJECT.uuId"]],
        }
        projects = api.query(payload)
        for t in projects:
            return t[0]
        return None

    @classmethod
    def add_task_template(cls, project, template):
        """Insert TaskTemplate `template` into Project `project`"""
        url = "/api/task/task_template/add?override=false&group=false"
        payload = {"uuId": project["uuId"], "templateList": [template]}
        api.post(url, payload)

    def reset_duration(self, calendars=None):
        """Set this task's duration based on its start and end dates while
        taking into account the calendar for weekends and scheduled time off.

        calendars is expected to be the list of calendar objects for the
        location of the project that holds this task. You may provide this
        list yourself for efficiency (recommended) - if not provided, it
        will be fetched for you by issuing requests to the server.
        """
        if not calendars:
            if "projectRef" not in self:
                task = projectal.Task.get(self)
                project_ref = task["projectRef"]
            else:
                project_ref = self["projectRef"]
            project = projectal.Project.get(project_ref, links=["LOCATION"])
            for location in project.get("locationList", []):
                calendars = location.calendar()
                break

        start = self.get("startTime")
        end = self.get("closeTime")
        if not start or start == DateLimit.Min:
            return 0
        if not end or end == DateLimit.Max:
            return 0

        # Build a list of weekday names that are non-working
        base_non_working = set()
        location_non_working = {}
        location_working = set()
        for calendar in calendars:
            if calendar["name"] == "base_calendar":
                for item in calendar["calendarList"]:
                    if not item["isWorking"]:
                        base_non_working.add(item["type"])

            if calendar["name"] == "location":
                for item in calendar["calendarList"]:
                    start_date = datetime.date.fromisoformat(item["startDate"])
                    end_date = datetime.date.fromisoformat(item["endDate"])
                    if not item["isWorking"]:
                        delta = start_date - end_date
                        location_non_working[item["startDate"]] = delta.days + 1
                    else:
                        location_working = {
                            (start_date + datetime.timedelta(days=x)).strftime(
                                "%Y-%m-%d"
                            )
                            for x in range((end_date - start_date).days + 1)
                        }

        start = datetime.datetime.fromtimestamp(start / 1000)
        end = datetime.datetime.fromtimestamp(end / 1000)
        minutes = 0
        current = start
        while current <= end:
            if (
                current.strftime("%A") in base_non_working
                and current.strftime("%Y-%m-%d") not in location_working
            ):
                current += datetime.timedelta(days=1)
                continue
            if current.strftime("%Y-%m-%d") in location_non_working:
                days = location_non_working[current.strftime("%Y-%m-%d")]
                current += datetime.timedelta(days=days)
                continue
            minutes += 8 * 60
            current += datetime.timedelta(days=1)

        self["duration"] = minutes
