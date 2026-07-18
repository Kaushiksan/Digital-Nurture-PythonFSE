import { NavLink } from "react-router-dom";

function Header() {

    return (

        <header className="header">

            <h1>Student Portal</h1>

            <nav>

                <NavLink to="/">
                    Home
                </NavLink>

                <NavLink to="/courses">
                    Courses
                </NavLink>

                <NavLink to="/profile">
                    Profile
                </NavLink>

            </nav>

        </header>

    );

}

export default Header;
