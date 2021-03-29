from uuid import uuid4

class Status:
    Success="success"
    Running="running"
    Failed="failed"

class Node(object):
    def __init__(self, name=None, **kwargs):
        self.uuid = uuid4()
        self.name = name or self.__class__.__name__

    def tick(self, bb):
        node_data = bb.setdefault(self.uuid, {})
        user_data = bb[self.uuid].setdefault("data", {})
        node_status = node_data.setdefault("status", Status.Success)

        if node_status != Status.Running:
            self.start(user_data)
        
        node_status = self.update(user_data)

        if node_status != Status.Running:
            self.end(user_data)
        
        node_data["status"] = node_status
        return node_status

    def start(self, bb):
        pass

    def update(self, bb):
        raise NotImplementedError()

    def end(self, bb):
        pass

    def __repr__(self):
        return "{}:{}".format(self.name, self.uuid.hex[:9])


class Composite(Node):
    def __init__(self, *args, **kwargs):
        super(Composite, self).__init__(*args, **kwargs)
        self.children = kwargs["children"] if "children" in kwargs else []

    def add(self, *nodes):
        self.children.extend(nodes)

class Sequence(Composite):
    """Runs each child in sequence until failure"""
    def start(self, bb):
        bb["index"] = 0

    def update(self, bb):
        status = Status.Success
        
        for c in self.children[bb["index"]:]:
            status = c.tick(bb)

            if status == Status.Success:
                bb["index"] += 1
            else:
                break

        return status

class Selector(Composite):
    """Runs each child in sequence until success"""
    def start(self, bb):
        bb["index"] = 0

    def update(self, bb):
        status = Status.Success
        
        for c in self.children[bb["index"]:]:
            status = c.tick(bb)

            if status == Status.Failed:
                bb["index"] += 1
            else:
                break

        return status

class Parallel(Composite):
    """Runs all children until failure."""
    def start(self, bb):
        bb["running"] = set(c.uuid for c in self.children)

    def update(self, bb):
        overall_status = Status.Running

        if not bb["running"]:
            return Status.Success
        
        for c in self.children:
            if c.uuid not in bb["running"]:
                continue

            status = c.tick(bb)

            if status == Status.Failed:
                overall_status = Status.Failed
            elif status == Status.Success:
                bb["running"] -= set([c.uuid])

        return overall_status

class Repeater(Composite):
    def __init__(self, *args, **kwargs):
        super(Repeater, self).__init__(*args, **kwargs)
        self.count = kwargs["count"] if "count" in kwargs else None

    def update(self, bb):
        for c in self.children:
            c.tick(bb)

        return Status.Running

if __name__ == "__main__":
    from time import sleep

    class Succeeder(Node):
        def update(self, bb):
            return Status.Success

    class Failer(Node):
        def update(self, bb):
            return Status.Failed
    s1 = Selector(name="s1")
    s1.add(Failer())
    s1.add(Failer())
    s1.add(Succeeder())
    
    s2 = Sequence(name="s2")
    s2.add(Succeeder())
    s2.add(Succeeder())
    
    s3 = Sequence()
    s3.add(s1)
    s3.add(s2)

    bb = {}
    while True:
        status = s3.tick(bb)
        if status != Status.Running:
            print(status)
            break
        sleep(1)



