// src/App.tsx

import React, { useState } from "react";
import axios from "axios";

const App: React.FC = () => {
  const [apiKey, setApiKey] = useState<string>("");
  const [premise, setPremise] = useState<string>("");
  const [storyOptions, setStoryOptions] = useState<string[]>([]);
  const [selectedStory, setSelectedStory] = useState<string | null>(null);
  const [story, setStory] = useState<string>(""); // Full story
  const [loading, setLoading] = useState<boolean>(false);
  const [Step, setStep] = useState<string>("Beginning");
  const surprisePremises = [
    "A detective solving a mystery in a haunted house.",
    "A young wizard discovering their powers.",
    "An alien invasion in a peaceful village.",
  ];

  const handleApiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setApiKey(e.target.value);
  };

  const handlePremiseChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPremise(e.target.value);
  };

  const handleSurpriseMe = () => {
    const randomPremise =
      surprisePremises[Math.floor(Math.random() * surprisePremises.length)];
    setPremise(randomPremise);
  };

  const generateStory = async (currentStep: string) => {
    if (!apiKey || !premise) {
      alert("Please enter both an API key and a premise.");
      return;
    }

    setLoading(true);
    setStoryOptions([]);
    setSelectedStory(null);

    try {
      const response = await axios.post(
        "https://api.worqhat.com/api/ai/content/v4",
        {
          question: `Generate a story based on this premise: ${premise} but only the ${currentStep}`,
          model: "aicon-v4-large-160824",
          randomness: 0.5,
          stream_data: false,
          training_data:
            "You are a great story writer and create 3 options, return them in a string array in key content . ",
          response_type: "json",
        },
        {
          headers: {
            Authorization: `Bearer ${apiKey}`,
          },
        }
      );
      console.log(response);
      setStoryOptions(JSON.parse(response.data.content).content || []);
    } catch (error) {
      console.error("Error fetching stories", error);
      alert("Failed to generate stories. Check your API key and premise.");
    } finally {
      setLoading(false);
    }
  };

  const handleStorySelect = (storyPart: string) => {
    setStory((prevStory) => prevStory + " " + storyPart); // Append the selected part to the full story
    setSelectedStory(storyPart);

    // Move to the next step
    if (Step === "Beginning") {
      setPremise((prev) => prev + " " + storyPart);
      setStep("Middle");
      generateStory("Middle");
    } else if (Step === "Middle") {
      setStep("Climax");
      generateStory("Climax");
    } else if (Step === "Climax") {
      setStep("Ending");
      generateStory("Ending");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Story Generator</h1>

      {Step === "Ending" ? (
        <div style={{ marginTop: "20px" }}>
          <h2>Your Full Story</h2>
          <p>{story}</p>
        </div>
      ) : (
        <>
          <div>
            <label>API Key:</label>
            <input
              type="text"
              value={apiKey}
              onChange={handleApiKeyChange}
              style={{ marginLeft: "10px", padding: "5px" }}
            />
          </div>

          <div style={{ marginTop: "20px" }}>
            <label>Premise:</label>
            <input
              type="text"
              value={premise}
              onChange={handlePremiseChange}
              placeholder="Enter a premise..."
              style={{ marginLeft: "10px", padding: "5px" }}
            />
            <button
              onClick={handleSurpriseMe}
              style={{ marginLeft: "10px", padding: "5px" }}
            >
              Surprise Me!
            </button>
          </div>

          <button
            onClick={() => generateStory(Step)}
            style={{ marginTop: "20px", padding: "10px 20px" }}
            disabled={loading}
          >
            {loading ? `Generating ${Step}...` : `Generate ${Step}`}
          </button>

          {storyOptions.length > 0 && (
            <div style={{ marginTop: "20px" }}>
              <h2>Story So Far:</h2>
              <p>{story}</p>
              <h2>Select a {Step} Option</h2>
              {storyOptions.map((storyOption, index) => (
                <div key={index} style={{ marginBottom: "10px" }}>
                  <button
                    onClick={() => handleStorySelect(storyOption)}
                    style={{ padding: "5px", width: "100%" }}
                  >
                    {storyOption}
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default App;
