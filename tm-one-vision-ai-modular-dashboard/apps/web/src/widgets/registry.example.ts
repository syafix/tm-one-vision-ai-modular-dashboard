export type WidgetType =
  | "KpiCard"
  | "TimeSeriesChart"
  | "WeatherCard"
  | "SocialTrend"
  | "AlertFeed"
  | "CameraHealth";

export interface WidgetConfig {
  id: string;
  type: WidgetType;
  title: string;
  metric?: string;
  refreshSeconds: number;
  layout: { x: number; y: number; w: number; h: number };
}

// Register approved components only. Do not dynamically import untrusted plugins.
export const approvedWidgetTypes: ReadonlySet<WidgetType> = new Set([
  "KpiCard", "TimeSeriesChart", "WeatherCard", "SocialTrend", "AlertFeed", "CameraHealth"
]);
