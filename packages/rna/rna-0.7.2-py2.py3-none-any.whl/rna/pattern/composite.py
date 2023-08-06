"""
See [here](https://refactoring.guru/design-patterns/composite).

Examples:
    >>> import rna
    >>> from rna.pattern.composite import Component, Leaf, Composite
    >>> class MyLeaf(Leaf):
    ...     def operation(self) -> str:
    ...         return "Leaf"

    >>> class MyComposite(Composite):
    ...     def operation(self) -> str:
    ...         results = []
    ...         for child in self._children:
    ...             results.append(child.operation())
    ...         return f"Branch({'+'.join(results)})"

    The client code works with all of the components via the base interface.
    >>> def client_code(component: Component) -> None:
    ...     print(f"RESULT: {component.operation()}", end="")

    Thanks to the fact that the child-management operations are declared in the
    base Component class, the client code can work with any component, simple or
    complex, without depending on their concrete classes.
    >>> def client_code2(component1: Component, component2: Component) -> None:
    ...     if component1.is_composite():
    ...         component1.add(component2)
    ...     print(f"RESULT: {component1.operation()}", end="")


    This way the client code can support the simple leaf components...
    >>> simple = MyLeaf()

    Client: I've got a simple component:
    >>> client_code(simple)
    RESULT: Leaf

    ...as well as the complex composites.
    >>> tree = MyComposite()

    >>> branch1 = MyComposite()
    >>> branch1.add(MyLeaf())
    >>> branch1.add(MyLeaf())

    >>> branch2 = MyComposite()
    >>> branch2.add(MyLeaf())

    >>> tree.add(branch1)
    >>> tree.add(branch2)

    Client: Now I've got a composite tree:
    >>> client_code(tree)
    RESULT: Branch(Branch(Leaf+Leaf)+Branch(Leaf))

    Client: I don't need to check the components classes even when managing the tree:
    >>> client_code2(tree, simple)
    RESULT: Branch(Branch(Leaf+Leaf)+Branch(Leaf)+Leaf)

    This pattern is generically implemented such that you can subclass Component and then
    auto-generate Leave and Composite classes from this.
    >>> from abc import abstractmethod
    >>> class Graphic(Component):
    ...     @abstractmethod
    ...     def render(self) -> None:
    ...         pass
    >>> class CompositeGraphic(Graphic.Composite):
    ...     def render(self):
    ...         for child in self._children:
    ...             child.render()
    >>> class Ellipse(Graphic.Leaf):
    ...     def __init__(self, name):
    ...         self.name = name
    ...
    ...     def render(self):
    ...         print("Ellipse", self.name)
    >>> ellipse1 = Ellipse("1")
    >>> ellipse2 = Ellipse("2")
    >>> ellipse3 = Ellipse("3")
    >>> ellipse4 = Ellipse("4")
    >>> graphic1 = CompositeGraphic()
    >>> graphic2 = CompositeGraphic()
    >>> graphic1.add(ellipse1)
    >>> graphic1.add(ellipse2)
    >>> graphic1.add(ellipse3)
    >>> graphic2.add(ellipse4)
    >>> graphic = CompositeGraphic()
    >>> graphic.add(graphic1)
    >>> graphic.add(graphic2)
    >>> graphic.render()
    Ellipse 1
    Ellipse 2
    Ellipse 3
    Ellipse 4

"""
import typing
from abc import ABCMeta, abstractmethod


class ComponentMeta(ABCMeta):
    """
    Meta class exposing class attributes as mixin generators
    """

    # pylint: disable=invalid-name
    def Subclass(cls, name: str, mixins: typing.Type, namespace: dict = None):
        """
        Auto-generate a sub class from this class together with mixins
        Args:
            name: name of new class
        """
        if namespace is None:
            namespace = {}
        return type(name, (cls,) + mixins, namespace)

    @property
    def Leaf(cls) -> typing.Type:  # pylint: disable=invalid-name
        """
        Auto-generate a Leaf mixin from this class.
        The Leaf class represents the end objects of a composition. A leaf can't
        have any children.  Usually, it's the Leaf objects that do the actual work, whereas
        Composite objects only delegate to their sub-components.
        """

        def add(self, component: cls):  # pylint: disable=no-self-use
            """
            Leafes can not add
            """
            raise TypeError(
                "Trying to add component {component} to Leaf".format(**locals())
            )

        def remove(self, component: cls):  # pylint: disable=no-self-use
            """
            Leafes can not remove
            """
            raise TypeError(
                "Trying to remove component {component} from Leaf".format(**locals())
            )

        return cls.Subclass("Leaf", (), dict(add=add, remove=remove))

    @property
    def Composite(cls) -> typing.Type:  # pylint: disable=invalid-name
        """
        Auto-generate a Composite subclass from this class.
        The Composite class represents the complex components that may have children. Usually, the
        Composite objects delegate the actual work to their children and then "sums-up" the result.
        """

        def __init__(self) -> None:
            self._children: typing.List[cls] = []

        def add(self, component: cls) -> None:
            """
            Add component by appending it to children
            """
            self._children.append(component)  # pylint:disable=protected-access
            component.parent = self

        def remove(self, component: cls) -> None:
            """
            Remove component by appending it to children
            """
            self._children.remove(component)  # pylint:disable=protected-access
            component.parent = None

        def is_composite(self) -> bool:  # pylint: disable=unused-argument
            """
            Whether a component can bear children.
            """
            return True

        return cls.Subclass(
            "Composite",
            (),
            dict(__init__=__init__, add=add, remove=remove, is_composite=is_composite),
        )


class Component(metaclass=ComponentMeta):
    """
    The base Component class declares common operations for both simple and complex objects of a
    composition.
    """

    @property
    def parent(self) -> "Component":
        """
        Returns:
            parent component
        """
        return self._parent

    @parent.setter
    def parent(self, parent: "Component"):
        """
        Optionally, the base Component can declare an interface for setting and
        accessing a parent of the component in a tree structure. It can also
        provide some default implementation for these methods.
        """
        self._parent = parent

    # In some cases, it would be beneficial to define the child-management
    # operations right in the base Component class. This way, you won't need to
    # expose any concrete component classes to the client code, even during the
    # object tree assembly.

    @abstractmethod
    def add(self, component: "Component") -> None:
        """
        Polymorphism for adding components to a subclass.
        """

    @abstractmethod
    def remove(self, component: "Component") -> None:
        """
        Polymorphism for removing components to a subclass.
        """

    def is_composite(self) -> bool:  # pylint: disable=no-self-use
        """
        Whether a component can bear children.
        """
        return False


class Leaf(Component.Leaf):
    """
    Implementation for pattern namespace. If you want to subclass Component, use auto-generated
    Component.Leaf type
    """


class Composite(Component.Composite):
    """
    Implementation for pattern namespace. If you want to subclass Component, use auto-generated
    Component.Composite type
    """
