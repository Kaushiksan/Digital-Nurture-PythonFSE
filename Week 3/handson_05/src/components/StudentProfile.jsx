import {
    useState
} from "react";


function StudentProfile() {

    const [
        name,
        setName
    ] = useState("");


    const [
        email,
        setEmail
    ] = useState("");


    const [
        semester,
        setSemester
    ] = useState("");


    return (

        <section
            id="profile"
            className="profile-section"
        >

            <h2>
                Student Profile
            </h2>


            <form className="profile-form">

                <label htmlFor="student-name">

                    Name

                </label>


                <input
                    id="student-name"
                    type="text"
                    value={name}
                    onChange={
                        (event) => {

                            setName(
                                event.target.value
                            );

                        }
                    }
                />


                <label htmlFor="student-email">

                    Email

                </label>


                <input
                    id="student-email"
                    type="email"
                    value={email}
                    onChange={
                        (event) => {

                            setEmail(
                                event.target.value
                            );

                        }
                    }
                />


                <label htmlFor="student-semester">

                    Semester

                </label>


                <input
                    id="student-semester"
                    type="number"
                    value={semester}
                    onChange={
                        (event) => {

                            setSemester(
                                event.target.value
                            );

                        }
                    }
                />

            </form>


            <div className="profile-preview">

                <h3>
                    Profile Preview
                </h3>

                <p>
                    Name: {name || "Not entered"}
                </p>

                <p>
                    Email: {email || "Not entered"}
                </p>

                <p>
                    Semester: {
                        semester || "Not entered"
                    }
                </p>

            </div>

        </section>

    );

}


export default StudentProfile;
