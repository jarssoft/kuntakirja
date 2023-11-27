import React, { useEffect, useCallback } from "react";
import css from "./Softkey.module.css";

export const Softkey = ({
  left,
  onKeyLeft,
  center,
  onKeyCenter,
  right,
  onKeyRight,
  selected
}) => {

    const handleKeyDown = useCallback(evt => {
        switch (evt.key) {
          case "SoftLeft":
            return onKeyLeft && onKeyLeft(evt);
          case "Enter":
            return onKeyCenter && onKeyCenter(evt);
          case "SoftRight":
            return onKeyRight && onKeyRight(evt);
          default:
            return;
        }
      }, [onKeyLeft,onKeyCenter,onKeyRight]);

      
  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);

    return () => document.removeEventListener("keydown", handleKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [handleKeyDown]);


  return (
    <div className={css.softkey}>
      <label className={css.left} onClick={()=>onKeyLeft && onKeyLeft()}>{left}</label>
      <label className={css.center} onClick={()=>onKeyCenter && onKeyCenter()}>{center}</label>
      <label className={css.right} onClick={()=>onKeyRight && onKeyRight()}>{right}</label>
    </div>
  );
};
