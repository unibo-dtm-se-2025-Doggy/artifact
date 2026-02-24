import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";

function Dummy() {
  return <div>Doggy Test OK</div>;
}

describe("Smoke test", () => {
  it("renders correctly", () => {
    render(<Dummy />);
    expect(screen.getByText("Doggy Test OK")).toBeInTheDocument();
  });
});