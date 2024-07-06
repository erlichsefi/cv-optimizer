from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, HttpUrl, PastDate, FutureDate, Field
from pydantic import BaseModel, ValidationError
from langchain.output_parsers import PydanticOutputParser


class Address(BaseModel):
    country: str = Field(..., description="Your countrey")
    region: str = Field(..., description="Your region")
    city: Optional[str] = Field(..., description="Your city")


class PersonalInfo(BaseModel):
    firstname: str = Field(..., description="Your First Name")
    lastname: str = Field(..., description="Your Last Name")
    email: EmailStr = Field(..., description="Your Email Address")
    phone: str = Field(..., description="Your Phone Number")
    address: Address = Field(..., description="Your Address")
    is_willing_to_relocate: bool = Field(..., description="False/True")
    linkedin_link: HttpUrl = Field(..., description="Your LinkedIn Profile Link")
    github_link: HttpUrl = Field(..., description="Your GitHub Profile Link")
    additional_websites: Optional[List[HttpUrl]] = Field(
        ..., description="Additional Website"
    )


class Education(BaseModel):
    degree: str = Field(..., description="Degree Type")
    institution: str = Field(..., description="University or College Name")
    location: str = Field(..., description="City, Country")
    start_date: PastDate = Field(..., description="Start Date")
    graduation_date: Union[PastDate, FutureDate] = Field(
        ..., description="Graduation Date"
    )
    grade: Union[str, float] = Field(
        ..., description="Grade (with decimal point) or GPA"
    )


class Experience(BaseModel):
    title: str = Field(..., description="Job Title")
    company: str = Field(..., description="Company Name")
    location: Address = Field(..., description="City, Country")
    start_date: PastDate = Field(..., description="Start Date")
    end_date: Union[PastDate, FutureDate] = Field(
        ..., description="End Month and Year or 'Ongoing'"
    )
    is_ongoing: bool = Field(..., description="is current place of work")
    responsibilities: List[str] = Field(
        ..., description="list of responsibilities in the job"
    )
    keywords: List[str] = Field(..., description="extracted Keyword")


class Skill(BaseModel):
    name: str = Field(..., description="Skill")
    years: int = Field(..., description="Integer in Years")


class GithubProject(BaseModel):
    title: str = Field(..., description="Project Title")
    description: str = Field(..., description="Project Description")
    technologies: List[str] = Field(..., description="Technology Used")
    github_link: HttpUrl = Field(..., description="GitHub Repository Link")


class Language(BaseModel):
    language: str = Field(..., description="Language")
    level: str = Field(
        ...,
        pattern="^(Native|Fluent|Intermediate|Basic)$",
        description="Level of Proficiency (e.g., Native, Fluent, Intermediate, Basic)",
    )


class Achievement(BaseModel):
    achievement: str = Field(..., description="Achievement Description")
    date: PastDate = Field(..., description="Date of Achievement")


class Publication(BaseModel):
    title: str = Field(..., description="Publication Title")
    publish_date: PastDate = Field(..., description="Publication Date")
    published_venue: str = Field(..., description="Published Venue if published")
    co_authors: str = Field(..., description="Co-Authors")
    description: str = Field(..., description="Publication Description")
    link: HttpUrl = Field(..., description="Publication Link")


class VolunteerExperience(BaseModel):
    organization: str = Field(..., description="Organization Name")
    role: str = Field(..., description="Volunteer Role")
    location: str = Field(..., description="City, Country")
    start_date: str = Field(
        ..., pattern="^(19|20)\\d{2}-(0[1-9]|1[0-2])$", description="Start Date"
    )
    end_date: Optional[str] = Field(
        None,
        pattern="^(19|20)\\d{2}-(0[1-9]|1[0-2])$",
        description="End Date or 'Ongoing'",
    )
    is_ongoing: bool = Field(..., description="False or True")
    description: str = Field(..., description="Description of Volunteer Work")


class CurriculumVitae(BaseModel):
    personal_info: PersonalInfo
    education: List[Education]
    experience: List[Experience]
    skills: List[Skill]
    certifications: List[str] = Field(..., description="Certification Name")
    projects: List[GithubProject]
    languages: List[Language]
    achievements: List[Achievement]
    publications: List[Publication]
    volunteer_experience: List[VolunteerExperience]
    hobbies: List[str] = Field(..., description="Hobby")
    summary: str = Field(..., description="Summary of Yourself")

    @classmethod
    def from_json(cls,cv_json):
        try:
            return cls(**cv_json)
        except ValidationError as e:
            print(e)

    @classmethod
    def templete_for_prompt(cls):
        pydantic_parser = PydanticOutputParser(pydantic_object=CV)
        return pydantic_parser.get_format_instructions()


    @classmethod
    def from_llm_response(cls,answer):
        pydantic_parser = PydanticOutputParser(pydantic_object=CV)
        return pydantic_parser.parse(answer)
