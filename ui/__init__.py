# ui/__init__.py
from .cli_interface import CLIInterface
from .formatters import StudyPlanFormatter

__all__ = ['CLIInterface', 'StudyPlanFormatter']

"""

What This Achieves

- Clean Schedule Display: Parses JSON and shows it as a proper schedule
- Multiple View Options:
  - Compact table overview
  - Detailed daily breakdown
  - Markdown export option
- Better UX:
  - User can choose detail level
  - Can export to file
  - Progress tracking menu
- Error Handling: Gracefully falls back if JSON parsing fails
- Professional Look: Uses Rich library for beautiful terminal UI

Example Output Flow (illustrative)

📊 Schedule Overview
┏━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Day ┃ Time             ┃ Topic                  ┃ Duration ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 1   │ 9:00 AM - 11:00  │ Intro to ML            │ 1-2 hrs  │
│ 1   │ 11:00 AM - 1:00  │ Supervised Learning    │ 1-2 hrs  │
└─────┴──────────────────┴────────────────────────┴──────────┘

Show detailed daily breakdown? (yes/no): yes

📅 Day 1 Schedule
────────────────────────────────────────

┌─ Session 1 ─────────────────────────────┐
│ ⏰ 9:00 AM - 11:00 AM                    │
│ 📚 Introduction to Machine Learning      │
│                                          │
│ Understanding ML fundamentals...         │
└──────────────────────────────────────────┘


## What This Achieves

✅ **Clean Schedule Display**: Parses JSON and shows it as a proper schedule
✅ **Multiple View Options**: 
   - Compact table overview
   - Detailed daily breakdown
   - Markdown export option
✅ **Better UX**: 
   - User can choose detail level
   - Can export to file
   - Progress tracking menu
✅ **Error Handling**: Gracefully falls back if JSON parsing fails
✅ **Professional Look**: Uses Rich library for beautiful terminal UI


## Example Output Flow

📊 Schedule Overview
┏━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Day ┃ Time             ┃ Topic                  ┃ Duration ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 1   │ 9:00 AM - 11:00  │ Intro to ML            │ 1-2 hrs  │
│ 1   │ 11:00 AM - 1:00  │ Supervised Learning    │ 1-2 hrs  │
└─────┴──────────────────┴────────────────────────┴──────────┘

Show detailed daily breakdown? (yes/no): yes

📅 Day 1 Schedule
────────────────────────────────────────

┌─ Session 1 ─────────────────────────────┐
│ ⏰ 9:00 AM - 11:00 AM                   │
│ 📚 Introduction to Machine Learning     │
│                                          │
│ Understanding ML fundamentals...         │
└──────────────────────────────────────────┘

"""