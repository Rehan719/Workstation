import json
import os
import datetime
import asyncio
from typing import List, Dict, Any
from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.ueg.logger import VSBUEGLogger

class SATsScheduleGenerator:
    """
    Generates a 14-day intensive revision schedule for the child.
    """
    def __init__(self, output_dir: str = "outputs/education/sats_2026/revision_schedule"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.ueg = VSBUEGLogger()

    @constitutional_guard
    async def generate_schedule(self) -> Dict[str, Any]:
        start_date = datetime.date(2026, 5, 1)
        schedule = []

        subjects = [
            "English GPS & Spelling",
            "English Reading",
            "Maths Arithmetic",
            "Maths Reasoning"
        ]

        # SATs Timetable 2026
        # Monday 11 May – English GPS
        # Tuesday 12 May – English Reading
        # Wednesday 13 May – Maths Arithmetic & Reasoning 1
        # Thursday 14 May – Maths Reasoning 2
        exam_timetable = {
            11: "EXAM: English GPS",
            12: "EXAM: English Reading",
            13: "EXAM: Maths Arithmetic & Reasoning 1",
            14: "EXAM: Maths Reasoning 2"
        }

        for i in range(14):
            current_date = start_date + datetime.timedelta(days=i)
            day_of_month = current_date.day
            day_schedule = {
                "day": i + 1,
                "date": current_date.isoformat(),
                "sessions": []
            }

            if day_of_month in exam_timetable:
                day_schedule["sessions"] = [
                    {"time": "09:00 - 11:00", "activity": f"SATs {exam_timetable[day_of_month]}", "goal": "Perform best"},
                    {"time": "13:00 - 14:00", "activity": "Arsenal / Minecraft Rest", "goal": "Recover (Oxygen Cycle)"},
                    {"time": "16:00 - 16:30", "activity": "Light Review for Tomorrow", "goal": "Final Prep"}
                ]
                day_schedule["status"] = "SATs EXAM WEEK"
            elif i < 10: # Revision days (1 May to 10 May)
                day_schedule["sessions"] = [
                    {"time": "09:00 - 09:30", "activity": f"Practice: {subjects[i % 4]} Set {i//4 + 1}", "goal": "Focus and Accuracy"},
                    {"time": "11:00 - 11:30", "activity": "Sensory Break / Minecraft / Football", "goal": "Rest & Recharge (Oxygen Cycle)"},
                    {"time": "16:00 - 16:30", "activity": f"Review: {subjects[(i+1) % 4]} Model Answers", "goal": "Knowledge Consistency (Carbon Cycle)"}
                ]
                day_schedule["status"] = "Intensive Revision"
            else: # Weekend/Final Prep days
                day_schedule["sessions"] = [
                    {"time": "10:00 - 10:30", "activity": "Confidence Booster Quiz", "goal": "Wellbeing (Sulphur Cycle)"},
                    {"time": "14:00 - 15:00", "activity": "Relaxation / Arsenal Match", "goal": "Homeostasis"}
                ]
                day_schedule["status"] = "Final Prep & Wellbeing"

            schedule.append(day_schedule)

        return {"revision_plan": schedule}

    async def save_markdown(self, schedule_data: Dict[str, Any]):
        md_content = "# 📅 SATs 2026: 14-Day Revision Schedule\n\n"
        md_content += "## Personalized for: Norbury School Pupil\n\n"

        for day in schedule_data["revision_plan"]:
            md_content += f"### Day {day['day']} - {day['date']} ({day['status']})\n"
            for session in day["sessions"]:
                md_content += f"- **{session['time']}**: {session['activity']} (Goal: {session['goal']})\n"
            md_content += "\n---\n"

        path = os.path.join(self.output_dir, "schedule.md")
        with open(path, "w") as f:
            f.write(md_content)

        # Also save JSON
        json_path = os.path.join(self.output_dir, "schedule.json")
        with open(json_path, "w") as f:
            json.dump(schedule_data, f, indent=4)

        return path

async def main():
    gen = SATsScheduleGenerator()
    data = await gen.generate_schedule()
    await gen.save_markdown(data)
    print("Schedule generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
