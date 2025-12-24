import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Home from "./pages/Home";
import ImageGeneration from "./pages/ImageGeneration";
import ImageEditing from "./pages/ImageEditing";
import TextToVideo from "./pages/TextToVideo";
import ImageToVideo from "./pages/ImageToVideo";
import TextToSpeech from "./pages/TextToSpeech";
import SpeechToText from "./pages/SpeechToText";
import Chat from "./pages/Chat";
import Embeddings from "./pages/Embeddings";

function Router() {
  return (
    <Switch>
      <Route path={"/"} component={Home} />
      <Route path={"/image-generation"} component={ImageGeneration} />
      <Route path={"/image-editing"} component={ImageEditing} />
      <Route path={"/text-to-video"} component={TextToVideo} />
      <Route path={"/image-to-video"} component={ImageToVideo} />
      <Route path={"/text-to-speech"} component={TextToSpeech} />
      <Route path={"/speech-to-text"} component={SpeechToText} />
      <Route path={"/chat"} component={Chat} />
      <Route path={"/embeddings"} component={Embeddings} />
      <Route path={"/404"} component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

// NOTE: About Theme
// - First choose a default theme according to your design style (dark or light bg), than change color palette in index.css
//   to keep consistent foreground/background color across components
// - If you want to make theme switchable, pass `switchable` ThemeProvider and use `useTheme` hook

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider
        defaultTheme="light"
        // switchable
      >
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
