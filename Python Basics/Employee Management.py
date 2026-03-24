
from abc import ABC, abstractmethod
from datetime import date


# ─────────────────────────────────────────────
# BASE CLASS (Abstract)
# ─────────────────────────────────────────────
class Employee(ABC):
    """Abstract base class for all employee types."""

    company_name = "TechCorp Inc."   # Class variable (shared)

    def __init__(self, emp_id: str, name: str, department: str, join_date: str):
        self.__emp_id    = emp_id          # Private (name mangling)
        self._name       = name            # Protected
        self._department = department      # Protected
        self._join_date  = join_date
        self._is_active  = True

    # ── Getters (Encapsulation) ──────────────
    @property
    def emp_id(self):      return self.__emp_id
    @property
    def name(self):        return self._name
    @property
    def department(self):  return self._department
    @property
    def join_date(self):   return self._join_date
    @property
    def is_active(self):   return self._is_active

    # ── Abstract methods (Polymorphism) ──────
    @abstractmethod
    def calculate_salary(self) -> float:
        """Every subclass MUST implement this."""
        pass

    @abstractmethod
    def get_role(self) -> str:
        """Every subclass MUST implement this."""
        pass

    # ── Concrete shared method ────────────────
    def get_details(self) -> dict:
        return {
            "ID"         : self.emp_id,
            "Name"       : self._name,
            "Role"       : self.get_role(),
            "Department" : self._department,
            "Joined"     : self._join_date,
            "Salary"     : f"₹{self.calculate_salary():,.2f}",
            "Status"     : "Active" if self._is_active else "Inactive",
        }

    def deactivate(self):
        self._is_active = False
        print(f"  ⚠  {self._name} has been deactivated.")

    def __str__(self):
        return (f"[{self.get_role()}] {self._name} "
                f"(ID: {self.emp_id}) — ₹{self.calculate_salary():,.2f}/mo")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.emp_id!r}, name={self._name!r})"


# ─────────────────────────────────────────────
# SUBCLASS 1 — Full-Time Employee
# ─────────────────────────────────────────────
class FullTimeEmployee(Employee):
    """Receives a fixed monthly salary + optional bonus."""

    def __init__(self, emp_id, name, department, join_date,
                 base_salary: float, bonus: float = 0.0):
        super().__init__(emp_id, name, department, join_date)
        self._base_salary = base_salary
        self._bonus       = bonus

    def get_role(self) -> str:
        return "Full-Time Employee"

    def calculate_salary(self) -> float:          # Polymorphism
        return self._base_salary + self._bonus

    def apply_raise(self, percent: float):
        self._base_salary *= (1 + percent / 100)
        print(f"  ✔  {self._name}'s salary raised by {percent}% "
              f"→ ₹{self._base_salary:,.2f}")


# ─────────────────────────────────────────────
# SUBCLASS 2 — Part-Time Employee
# ─────────────────────────────────────────────
class PartTimeEmployee(Employee):
    """Paid by hours worked × hourly rate."""

    def __init__(self, emp_id, name, department, join_date,
                 hourly_rate: float, hours_worked: float):
        super().__init__(emp_id, name, department, join_date)
        self._hourly_rate  = hourly_rate
        self._hours_worked = hours_worked

    def get_role(self) -> str:
        return "Part-Time Employee"

    def calculate_salary(self) -> float:          # Polymorphism
        return self._hourly_rate * self._hours_worked

    def log_hours(self, extra_hours: float):
        self._hours_worked += extra_hours
        print(f"  ✔  Logged {extra_hours}h for {self._name} "
              f"(total: {self._hours_worked}h)")


# ─────────────────────────────────────────────
# SUBCLASS 3 — Manager  (inherits FullTime)
# ─────────────────────────────────────────────
class Manager(FullTimeEmployee):
    """Extends FullTimeEmployee with a team and allowance."""

    def __init__(self, emp_id, name, department, join_date,
                 base_salary: float, team_size: int, allowance: float = 5000):
        super().__init__(emp_id, name, department, join_date, base_salary)
        self._team_size  = team_size
        self._allowance  = allowance
        self._team: list = []

    def get_role(self) -> str:
        return "Manager"

    def calculate_salary(self) -> float:          # Polymorphism (override)
        return self._base_salary + self._allowance

    def add_team_member(self, employee: Employee):
        self._team.append(employee)
        print(f"  ✔  {employee.name} added to {self._name}'s team.")

    def show_team(self):
        print(f"\n  📋 {self._name}'s Team ({len(self._team)} members):")
        for emp in self._team:
            print(f"     • {emp}")


# ─────────────────────────────────────────────
# SUBCLASS 4 — Intern
# ─────────────────────────────────────────────
class Intern(Employee):
    """Fixed stipend, linked to a mentor."""

    def __init__(self, emp_id, name, department, join_date,
                 stipend: float, mentor_name: str, duration_months: int):
        super().__init__(emp_id, name, department, join_date)
        self._stipend        = stipend
        self._mentor_name    = mentor_name
        self._duration       = duration_months

    def get_role(self) -> str:
        return "Intern"

    def calculate_salary(self) -> float:          # Polymorphism
        return self._stipend

    def get_details(self) -> dict:                # Method Overriding
        d = super().get_details()
        d["Mentor"]   = self._mentor_name
        d["Duration"] = f"{self._duration} months"
        return d


# ─────────────────────────────────────────────
# SUBCLASS 5 — Contractor
# ─────────────────────────────────────────────
class Contractor(Employee):
    """Project-based payment: rate × project days."""

    def __init__(self, emp_id, name, department, join_date,
                 daily_rate: float, project_days: int, project_name: str):
        super().__init__(emp_id, name, department, join_date)
        self._daily_rate   = daily_rate
        self._project_days = project_days
        self._project_name = project_name

    def get_role(self) -> str:
        return "Contractor"

    def calculate_salary(self) -> float:          # Polymorphism
        return self._daily_rate * self._project_days

    def extend_contract(self, extra_days: int):
        self._project_days += extra_days
        print(f"  ✔  Contract extended by {extra_days} days "
              f"for {self._name}. New total: {self._project_days} days.")


# ─────────────────────────────────────────────
# MANAGEMENT SYSTEM
# ─────────────────────────────────────────────
class EmployeeManagementSystem:
    """Central registry — demonstrates polymorphism in loops."""

    def __init__(self):
        self._employees: dict[str, Employee] = {}

    def add_employee(self, emp: Employee):
        self._employees[emp.emp_id] = emp
        print(f"  ✔  Added: {emp}")

    def remove_employee(self, emp_id: str):
        emp = self._employees.pop(emp_id, None)
        if emp:
            emp.deactivate()
            print(f"  ✔  Removed {emp.name} from records.")
        else:
            print(f"  ✗  Employee {emp_id} not found.")

    def get_employee(self, emp_id: str) -> Employee | None:
        return self._employees.get(emp_id)

    def total_payroll(self) -> float:
        # Polymorphism: each type's calculate_salary() is called transparently
        return sum(e.calculate_salary() for e in self._employees.values()
                   if e.is_active)

    def list_by_role(self):
        roles: dict[str, list] = {}
        for emp in self._employees.values():
            roles.setdefault(emp.get_role(), []).append(emp)
        for role, emps in roles.items():
            print(f"\n  [{role}]")
            for e in emps:
                print(f"    • {e}")

    def department_report(self):
        depts: dict[str, list] = {}
        for emp in self._employees.values():
            depts.setdefault(emp.department, []).append(emp)
        print(f"\n{'─'*50}")
        print(f"  DEPARTMENT REPORT — {Employee.company_name}")
        print(f"{'─'*50}")
        for dept, emps in depts.items():
            total = sum(e.calculate_salary() for e in emps if e.is_active)
            print(f"\n  🏢 {dept}  ({len(emps)} employees) — ₹{total:,.2f}/mo")
            for e in emps:
                print(f"     • {e.name:<20} {e.get_role():<22} ₹{e.calculate_salary():>10,.2f}")

    def print_payroll(self):
        print(f"\n{'═'*50}")
        print(f"  MONTHLY PAYROLL — {Employee.company_name}")
        print(f"{'═'*50}")
        for emp in self._employees.values():
            status = "✔" if emp.is_active else "✗"
            print(f"  {status}  {emp.name:<20} {emp.get_role():<22} "
                  f"₹{emp.calculate_salary():>10,.2f}")
        print(f"{'─'*50}")
        print(f"  {'TOTAL PAYROLL':<43} ₹{self.total_payroll():>10,.2f}")
        print(f"{'═'*50}\n")


# ─────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────
if __name__ == "__main__":
    ems = EmployeeManagementSystem()

    print("\n" + "═"*50)
    print("  EMPLOYEE MANAGEMENT SYSTEM DEMO")
    print("═"*50)

    # Create employees
    print("\n📌 Adding Employees...\n")
    mgr   = Manager    ("M001", "Priya Sharma",    "Engineering",  "2021-03-15", 120000, 8, 15000)
    ft1   = FullTimeEmployee("E001", "Arjun Mehta", "Engineering", "2022-06-01", 85000, 5000)
    ft2   = FullTimeEmployee("E002", "Sneha Joshi",  "HR",          "2023-01-10", 70000)
    pt1   = PartTimeEmployee ("P001", "Rahul Verma", "Marketing",  "2024-02-20", 600, 80)
    intern= Intern     ("I001", "Kavya Nair",      "Engineering",  "2024-07-01", 15000, "Priya Sharma", 6)
    cont  = Contractor ("C001", "Dev Malhotra",    "Design",       "2024-08-15", 4500, 30, "Website Redesign")

    for emp in [mgr, ft1, ft2, pt1, intern, cont]:
        ems.add_employee(emp)

    # Manager builds team
    print("\n📌 Building Manager's Team...\n")
    mgr.add_team_member(ft1)
    mgr.add_team_member(intern)
    mgr.show_team()

    # Various operations
    print("\n📌 Operations...\n")
    ft1.apply_raise(10)
    pt1.log_hours(20)
    cont.extend_contract(15)

    # Polymorphic payroll
    ems.print_payroll()

    # Department report
    ems.department_report()

    # Details of one employee
    print("\n📌 Intern Details:\n")
    for k, v in intern.get_details().items():
        print(f"  {k:<12}: {v}")

    # Deactivate one
    print("\n📌 Removing Contractor...\n")
    ems.remove_employee("C001")
    ems.print_payroll()
