"""Import all classes and functions the end user will need to make an app.

Anything imported here will be available in the default Reflex import as `xt.*`.
To signal to typecheckers that something should be reexported,
we use the Flask "import name as name" syntax.
"""
import importlib
from typing import Type

from nextpy.core.page import page as page
from nextpy.utils.format import to_snake_case

_ALL_COMPONENTS = [
    "Accordion",
    "AccordionButton",
    "AccordionIcon",
    "AccordionItem",
    "AccordionPanel",
    "Alert",
    "AlertDescription",
    "AlertDialog",
    "AlertDialogBody",
    "AlertDialogContent",
    "AlertDialogFooter",
    "AlertDialogHeader",
    "AlertDialogOverlay",
    "AlertIcon",
    "AlertTitle",
    "AspectRatio",
    "Audio",
    "Avatar",
    "AvatarBadge",
    "AvatarGroup",
    "Badge",
    "Box",
    "Breadcrumb",
    "BreadcrumbItem",
    "BreadcrumbLink",
    "BreadcrumbSeparator",
    "Button",
    "ButtonGroup",
    "Card",
    "CardBody",
    "CardFooter",
    "CardHeader",
    "Center",
    "Checkbox",
    "CheckboxGroup",
    "CircularProgress",
    "CircularProgressLabel",
    "Circle",
    "Code",
    "CodeBlock",
    "Collapse",
    "ColorModeButton",
    "ColorModeIcon",
    "ColorModeSwitch",
    "Component",
    "Cond",
    "ConnectionBanner",
    "ConnectionModal",
    "Container",
    "DataTable",
    "DataEditor",
    "DebounceInput",
    "Divider",
    "Drawer",
    "DrawerBody",
    "DrawerCloseButton",
    "DrawerContent",
    "DrawerFooter",
    "DrawerHeader",
    "DrawerOverlay",
    "Editable",
    "EditableInput",
    "EditablePreview",
    "EditableTextarea",
    "Editor",
    "Email",
    "Fade",
    "Flex",
    "Foreach",
    "Form",
    "FormControl",
    "FormErrorMessage",
    "FormHelperText",
    "FormLabel",
    "Fragment",
    "Grid",
    "GridItem",
    "Heading",
    "Highlight",
    "Hstack",
    "Html",
    "Icon",
    "IconButton",
    "Image",
    "Input",
    "InputGroup",
    "InputLeftAddon",
    "InputLeftElement",
    "InputRightAddon",
    "InputRightElement",
    "Kbd",
    "Link",
    "LinkBox",
    "LinkOverlay",
    "List",
    "ListItem",
    "Markdown",
    "Menu",
    "MenuButton",
    "MenuDivider",
    "MenuGroup",
    "MenuItem",
    "MenuItemOption",
    "MenuList",
    "MenuOptionGroup",
    "Modal",
    "ModalBody",
    "ModalCloseButton",
    "ModalContent",
    "ModalFooter",
    "ModalHeader",
    "ModalOverlay",
    "Moment",
    "MultiSelect",
    "MultiSelectOption",
    "NextLink",
    "NumberDecrementStepper",
    "NumberIncrementStepper",
    "NumberInput",
    "NumberInputField",
    "NumberInputStepper",
    "Option",
    "OrderedList",
    "Password",
    "PinInput",
    "PinInputField",
    "Plotly",
    "Popover",
    "PopoverAnchor",
    "PopoverArrow",
    "PopoverBody",
    "PopoverCloseButton",
    "PopoverContent",
    "PopoverFooter",
    "PopoverHeader",
    "PopoverTrigger",
    "Progress",
    "Radio",
    "RadioGroup",
    "RangeSlider",
    "RangeSliderFilledTrack",
    "RangeSliderThumb",
    "RangeSliderTrack",
    "ResponsiveGrid",
    "ScaleFade",
    "Script",
    "Select",
    "Skeleton",
    "SkeletonCircle",
    "SkeletonText",
    "Slide",
    "SlideFade",
    "Slider",
    "SliderFilledTrack",
    "SliderMark",
    "SliderThumb",
    "SliderTrack",
    "Spacer",
    "Span",
    "Spinner",
    "Square",
    "Stack",
    "Stat",
    "StatArrow",
    "StatGroup",
    "StatHelpText",
    "StatLabel",
    "StatArrow",
    "StatGroup",
    "StatHelpText",
    "StatLabel",
    "StatNumber",
    "Step",
    "StepDescription",
    "StepIcon",
    "StepIndicator",
    "StepNumber",
    "StepSeparator",
    "StepStatus",
    "StepTitle",
    "Stepper",
    "Switch",
    "Tab",
    "TabList",
    "TabPanel",
    "TabPanels",
    "Table",
    "TableCaption",
    "TableContainer",
    "Tabs",
    "Tag",
    "TagCloseButton",
    "TagLabel",
    "TagLeftIcon",
    "TagRightIcon",
    "Tbody",
    "Td",
    "Text",
    "TextArea",
    "Tfoot",
    "Th",
    "Thead",
    "Tooltip",
    "Tr",
    "UnorderedList",
    "Upload",
    "Video",
    "VisuallyHidden",
    "Vstack",
    "Wrap",
    "WrapItem",
]

_ALL_COMPONENTS += [to_snake_case(component) for component in _ALL_COMPONENTS]
_ALL_COMPONENTS += [
    "components",
    "desktop_only",
    "mobile_only",
    "tablet_only",
    "mobile_and_tablet",
    "tablet_and_desktop",
    "selected_files",
    "clear_selected_files",
    "EditorOptions",
]

_MAPPING = {
    "nextpy.core.admin": ["admin", "AdminDash"],
    "nextpy.app": ["app", "SingletonApp", "UploadFile"],
    "nextpy.core.base": ["base", "Base"],
    "nextpy.core.compiler": ["compiler"],
    "nextpy.core.compiler.utils": ["get_asset_path"],
    "nextpy.components": _ALL_COMPONENTS,
    "nextpy.components.component": ["memo"],
    "nextpy.components.graphing": ["recharts"],
    "nextpy.core.config": ["config", "Config", "DBConfig"],
    "nextpy.constants": ["constants", "Env"],
    "nextpy.core.el": ["el"],
    "nextpy.core.event": [
        "event",
        "EventChain",
        "background",
        "call_script",
        "clear_local_storage",
        "console_log",
        "download",
        "prevent_default",
        "redirect",
        "remove_cookie",
        "remove_local_storage",
        "set_clipboard",
        "set_focus",
        "set_value",
        "stop_propagation",
        "upload_files",
        "window_alert",
    ],
    "nextpy.core.middleware": ["middleware", "Middleware"],
    "nextpy.core.model": ["model", "session", "Model"],
    "nextpy.core.page": ["page"],
    "nextpy.core.route": ["route"],
    "nextpy.core.state": ["state", "var", "Cookie", "LocalStorage", "State"],
    "nextpy.core.style": ["style", "color_mode", "toggle_color_mode"],
    "nextpy.core.testing": ["testing"],
    "nextpy.utils": ["utils"],
    "nextpy.core.vars": ["vars", "cached_var", "Var"],
}
_MAPPING = {value: key for key, values in _MAPPING.items() for value in values}


def _removeprefix(text, prefix):
       return text[len(prefix):] if text.startswith(prefix) else text


__all__ = [_removeprefix(mod, "nextpy.") for mod in _MAPPING]


def __getattr__(name: str) -> Type:
    """Lazy load all modules.

    Args:
        name: name of the module to load.

    Returns:
        The module or the attribute of the module.

    Raises:
        AttributeError: If the module or the attribute does not exist.
    """
    # Alias handling for App as SingletonApp
    # TODO: If more aliases are needed in the future, consider using a __alias_mapping dictionary
    if name == "App":
        name = "SingletonApp"
        
    try:
        # Check for import of a module that is not in the mapping.
        if name not in _MAPPING:
            # If the name does not start with nextpy, add it.
            if not name.startswith("nextpy") and name != "__all__":
                name = f"nextpy.{name}"
            return importlib.import_module(name)

        # Import the module.
        module = importlib.import_module(_MAPPING[name])

        # Get the attribute from the module if the name is not the module itself.
        return (
            getattr(module, name) if name != _MAPPING[name].rsplit(".")[-1] else module
        )
    except ModuleNotFoundError:
        raise AttributeError(f"module 'nextpy' has no attribute {name}") from None