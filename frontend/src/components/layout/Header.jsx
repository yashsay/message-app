import brainLogo from "../../assets/brain.svg";
import "./Header.scss";

const Header = () => (
  <header className="header">
    <div className="header__logo">
      <img
        src={brainLogo}
        alt="IntelliChat Logo"
        className="header__logo-img"
      />
      <h1 className="header__title">IntelliChat</h1>
    </div>
    <div className="header__profile" tabIndex={0} title="Profile">
      {/* Placeholder profile icon, replace with user image if available */}
      <svg
        width="22"
        height="22"
        viewBox="0 0 22 22"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="11" cy="7.5" r="4" fill="#fff" fillOpacity=".7" />
        <ellipse
          cx="11"
          cy="15.5"
          rx="6.5"
          ry="3.5"
          fill="#fff"
          fillOpacity=".5"
        />
      </svg>
    </div>
  </header>
);

export default Header;
