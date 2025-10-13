"""CSS class constants for consistent styling across the application.

Only includes multi-class patterns that are duplicated multiple times.
Single utility classes (like 'mt-2', 'mb-4') are used inline to avoid thin abstractions.
"""

from typing import Final

# Button styles - commonly used button combinations
BUTTON_PRIMARY_SMALL: Final[str] = "btn btn-xs btn-primary mr-1"
BUTTON_PRIMARY_SMALL_MR2: Final[str] = "btn btn-xs btn-primary mr-2"
BUTTON_ERROR_SMALL: Final[str] = "btn btn-xs btn-error"
BUTTON_SUCCESS_SMALL: Final[str] = "btn btn-success btn-xs mr-2"
BUTTON_GHOST_SMALL: Final[str] = "btn btn-ghost btn-xs"
BUTTON_SUCCESS: Final[str] = "btn btn-success mr-2"
BUTTON_GHOST: Final[str] = "btn btn-ghost"
BUTTON_PRIMARY: Final[str] = "btn btn-primary mb-3"
BUTTON_INFO_MR2: Final[str] = "btn btn-info mr-2"
BUTTON_ERROR: Final[str] = "btn btn-error"
BUTTON_OUTLINE_TEMPLATE: Final[str] = "btn btn-outline w-full text-left h-auto py-4 mb-3"

# Card styles - base card with common padding/border pattern
CARD_BASE: Final[str] = "card border-2 p-3"
CARD_FORM: Final[str] = "card bg-base-100 shadow-lg p-4 mb-3"
CARD_FORM_SMALL: Final[str] = "card bg-base-100 shadow-lg p-2"

# Form input styles - commonly repeated form field patterns
SELECT_BORDERED: Final[str] = "select select-bordered w-full mb-1"
SELECT_BORDERED_MB2: Final[str] = "select select-bordered w-full mb-2"
SELECT_BORDERED_SMALL: Final[str] = "select select-bordered select-sm w-full"
TEXTAREA_BORDERED: Final[str] = "textarea textarea-bordered w-full mb-1"
TEXTAREA_BORDERED_MB2: Final[str] = "textarea textarea-bordered w-full mb-2"
TEXTAREA_BORDERED_SMALL: Final[str] = "textarea textarea-bordered textarea-sm w-full"
INPUT_BORDERED: Final[str] = "input input-bordered w-full mb-1"
INPUT_BORDERED_MB2: Final[str] = "input input-bordered w-full mb-2"
INPUT_BORDERED_SMALL: Final[str] = "input input-bordered input-sm w-full"
