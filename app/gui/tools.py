from .staple import StapleTypeID, Staple, Protector, ConnectionElement


class Tool:
    def __init__(self, grid):
        self.grid = grid

    def action(self, triangle):
        print("->")
        print("Tool action is abstract.")
        print("Needs implementation.")


class EraserTool(Tool):
    def __init__(self, grid):
        super().__init__(grid)

    def action(self, triangle):
        # remove staples
        for pos, staple_type in zip(triangle.get_neighbor_cords(), StapleTypeID):
            neighbor = self.grid.triangle_by_pos(pos)
            # when we have actual staples opposite staple becomes protector
            staple = neighbor.get_staple_by_type(staple_type)
            if type(staple) is Staple:
                print("delete into protector")
                triangle.set_staple_by_type(staple_type,
                                            Protector(triangle,type_id=staple.type_id))

            else:
                print("delete staple")
                # otherwise we delete the staple
                triangle.set_staple_by_type(staple_type, None)

                neighbor.set_staple_by_type(staple_type, None)
            neighbor.update()
        triangle.update()


class SelectorTool(Tool):
    def __init__(self, grid):
        super().__init__(grid)

    def action(self, triangle):
        #if one of the staples is no protector -> means we have to erase and not select
        for staple_type in StapleTypeID:
            staple = triangle.get_staple_by_type(staple_type)
            if staple and not type(staple) is Protector:
                    self.grid.eraser_tool.action(triangle)
                    return

        # add sides
        for staple_type in StapleTypeID:
            triangle.set_staple_by_type(staple_type, Staple(triangle, type_id=staple_type))

        # add protectors
        for pos, staple_type in zip(triangle.get_neighbor_cords(), StapleTypeID):
            neighbor = self.grid.triangle_by_pos(pos)
            if not neighbor.get_staple_by_type(staple_type):
                staple = Protector(neighbor, type_id=staple_type)
                neighbor.set_staple_by_type(staple_type, staple)
                neighbor.update()

        triangle.update()


class ConnectionAdditionTool(Tool):
    def __init__(self, grid):
        super().__init__(grid)
        self.connection = None
        self.p_triangle = None

    def terminate_connection(self):
        print("->Terminated Connection.")
        if self.connection:
            self.connection.triangle.set_staple_by_type(
                self.connection.type_id, self.connection.prev_protector)
            self.connection.triangle.update()
            self.connection = None
            self.p_triangle = None

    def action(self, triangle):
        # same triangle cliched twice -> undo
        if  self.p_triangle and self.p_triangle is triangle:
            self.terminate_connection()
            return

        # if triangle contains either one of the protectors it actually
        # needs to be selected first
        for staple_type in StapleTypeID:
            staple = triangle.get_staple_by_type(staple_type)
            if staple and type(staple) is Protector:
                print("-> Add a new triangle, to start connection.")
                self.grid.selection_tool.action(triangle)
                break

        # open connection
        # search for the friendly neighbor with the protector strand
        # has to be only 1 neighbor with 1 protector (otherwise selection order is A, B, C
        for pos, staple_type in zip(triangle.get_neighbor_cords(), StapleTypeID):
            neighbor = self.grid.triangle_by_pos(pos)
            staple = neighbor.get_staple_by_type(staple_type)
            if type(staple) is Protector:
                print("connection state:", self.connection)
                if not self.connection:
                    print("->Connector started.")
                    # replace the Ptotector with a ConnectionElement
                    self.connection = ConnectionElement(staple)
                    neighbor.set_staple_by_type(staple_type, self.connection)
                    neighbor.update()
                    self.p_triangle = triangle
                else:
                    print("->Connection closed.")
                    self.connection.connect_triangles(staple) #!!!
                    self.p_triangle = None
                    self.connection = None
                break

class FilterTool(Tool):
    def __init__(self, grid):
        super().__init__(grid)
        self.activated = False
    def action(self):
        if self.activated:
            #togle state -> action :)
            self.undo()
            self.activated = False
            return

        self.activated = True
        for row in self.grid.cells:
            for cell in row:
                for triangle in (cell.Left, cell.Right):
                    triangle.setEnabled(False)
                    for stype in StapleTypeID:
                        staple = triangle.get_staple_by_type(stype)
                        if staple:
                            if staple.short and staple.long1 and staple.long2:
                                triangle.setEnabled(True)
                        triangle.update()

    def undo(self):
        for row in self.grid.cells:
            for cell in row:
                for triangle in (cell.Left, cell.Right):
                    triangle.setEnabled(True)

class PrintSequencesTool(Tool):
    def __init__(self, grid):
        super().__init__(grid)

    def action(self, triangle):
        print(str(triangle))



