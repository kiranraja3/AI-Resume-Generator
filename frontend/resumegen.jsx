import React, { useState } from 'react';
import './ResumeGenerator.css';

const ResumeGenerator = () => {
    const [formData, setFormData] = useState({
        name: '',
        grade: '',
        email: '',
        gpa: '',
        school: '',
        coursework: '',
        clubs: '',
        honors: '',
        experiences: [{ title: '', description: '' }],
        skills: '',
        awards: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleExperienceChange = (e, index) => {
        const { name, value } = e.target;
        const updatedExperiences = [...formData.experiences];
        updatedExperiences[index][name] = value;
        setFormData({ ...formData, experiences: updatedExperiences });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Send form data to the backend API to generate the resume
        //placeholders
        const response = await fetch('/generate-resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.blob();
        const fileURL = URL.createObjectURL(result);
        const link = document.createElement('a');
        link.href = fileURL;
        link.download = 'resume.pdf';
        link.click();
    };

    return (
        <div className="resume-generator">
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Your Name"
                        className="input-box"
                    />
                </div>
                <div className="form-group">
                    <input
                        type="text"
                        name="grade"
                        value={formData.grade}
                        onChange={handleChange}
                        placeholder="Grade"
                        className="input-box"
                    />
                </div>
                <div className="form-group">
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="Email"
                        className="input-box"
                    />
                </div>
                <div className="form-group">
                    <input
                        type="text"
                        name="gpa"
                        value={formData.gpa}
                        onChange={handleChange}
                        placeholder="GPA"
                        className="input-box"
                    />
                </div>
                <div className="form-group">
                    <input
                        type="text"
                        name="school"
                        value={formData.school}
                        onChange={handleChange}
                        placeholder="School"
                        className="input-box"
                    />
                </div>
                <div className="form-group">
                    <textarea
                        name="coursework"
                        value={formData.coursework}
                        onChange={handleChange}
                        placeholder="Relevant Coursework"
                        className="input-box"
                    />
                </div>
                <div className="form-group">
                    <textarea
                        name="clubs"
                        value={formData.clubs}
                        onChange={handleChange}
                        placeholder="Clubs"
                        className="input-box"
                    />
                </div>
                <div className="form-group">
                    <textarea
                        name="honors"
                        value={formData.honors}
                        onChange={handleChange}
                        placeholder="Honors"
                        className="input-box"
                    />
                </div>

                {formData.experiences.map((experience, index) => (
                    <div key={index} className="form-group">
                        <input
                            type="text"
                            name="title"
                            value={experience.title}
                            onChange={(e) => handleExperienceChange(e, index)}
                            placeholder="Experience Title"
                            className="input-box"
                        />
                        <textarea
                            name="description"
                            value={experience.description}
                            onChange={(e) => handleExperienceChange(e, index)}
                            placeholder="Description"
                            className="input-box"
                        />
                    </div>
                ))}

                <div className="form-group">
                    <textarea
                        name="skills"
                        value={formData.skills}
                        onChange={handleChange}
                        placeholder="Skills"
                        className="input-box"
                    />
                </div>
                <div className="form-group">
                    <textarea
                        name="awards"
                        value={formData.awards}
                        onChange={handleChange}
                        placeholder="Awards"
                        className="input-box"
                    />
                </div>

                <button type="submit" className="submit-btn">Generate Resume</button>
            </form>
        </div>
    );
};

export default ResumeGenerator;
