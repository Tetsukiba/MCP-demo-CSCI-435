const imgShape = "https://www.figma.com/api/mcp/asset/aad7e40a-2a47-46ce-be54-fe1ffb5a2df1";
const imgSection = "https://www.figma.com/api/mcp/asset/7f0290af-cedd-4e0f-a013-f909022e88fa";
import { img, img1, img2, img3, img4, img5 } from "./svg-g5537";
type TextLinkListItemProps = {
  className?: string;
  text?: string;
};

function TextLinkListItem({ className, text = "List item" }: TextLinkListItemProps) {
  return (
    <div className={className} data-name="Text Link List Item" data-node-id="9:2078">
      <div className="absolute bottom-0 flex flex-col font-[family-name:var(--sds-typography-body-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-body-font-weight-regular,400)] justify-center leading-[0] left-0 not-italic right-[26.97%] text-[color:var(--sds-color-text-default-default,#1e1e1e)] text-[length:var(--sds-typography-body-size-medium,16px)] top-0 whitespace-nowrap" data-node-id="9:2079">
        <p className="leading-[1.4]">{text}</p>
      </div>
    </div>
  );
}
type TextStrongProps = {
  className?: string;
  text?: string;
};

function TextStrong({ className, text = "Text Strong" }: TextStrongProps) {
  return (
    <div className={className} data-name="Text Strong" data-node-id="9:2076">
      <p className="font-[family-name:var(--sds-typography-body-font-family,'Inter:Semi_Bold',sans-serif)] font-[var(--sds-typography-body-font-weight-strong,600)] leading-[1.4] not-italic relative shrink-0 text-[color:var(--sds-color-text-default-default,#1e1e1e)] text-[length:var(--sds-typography-body-size-medium,16px)]" data-node-id="9:2077">
        {text}
      </p>
    </div>
  );
}
type TextLinkListProps = {
  className?: string;
  hasTitle?: boolean;
  density?: "Default" | "Tight";
};

function TextLinkList({ className, hasTitle = true, density = "Default" }: TextLinkListProps) {
  return (
    <div className={className} data-name="Density=Default" data-node-id="9:2082">
      {hasTitle && (
        <div className="box-border content-stretch flex flex-col gap-[10px] items-start pb-[var(--sds-size-space-400,16px)] pt-0 px-0 relative shrink-0 w-full" data-name="Title" data-node-id="9:2084">
          <TextStrong className="content-stretch flex items-start relative shrink-0 w-full" />
        </div>
      )}
      <TextLinkListItem className="h-[22px] relative shrink-0 w-[89px]" />
      <TextLinkListItem className="h-[22px] relative shrink-0 w-[89px]" />
      <TextLinkListItem className="h-[22px] relative shrink-0 w-[89px]" />
      <TextLinkListItem className="h-[22px] relative shrink-0 w-[89px]" />
      <TextLinkListItem className="h-[22px] relative shrink-0 w-[89px]" />
      <TextLinkListItem className="h-[22px] relative shrink-0 w-[89px]" />
      <TextLinkListItem className="h-[22px] relative shrink-0 w-[89px]" />
    </div>
  );
}
type AvatarProps = {
  className?: string;
  type?: "Image";
  size?: "Large";
  shape?: "Circle";
};

function Avatar({ className, type = "Image", size = "Large", shape = "Circle" }: AvatarProps) {
  return (
    <div className={className} data-name="Type=Image, Size=Large, Shape=Circle" data-node-id="9:1895">
      <div className="absolute left-1/2 size-[40px] top-1/2 translate-x-[-50%] translate-y-[-50%]" data-name="Shape" data-node-id="9:1907">
        <img alt="" className="absolute inset-0 max-w-none object-50%-50% object-cover pointer-events-none size-full" src={imgShape} />
      </div>
    </div>
  );
}

function TestimonialCard({ className }: { className?: string }) {
  return (
    <div className={className} data-name="Testimonial Card" data-node-id="9:2054">
      <div className="content-stretch flex items-start relative shrink-0 w-full" data-name="Text Heading" data-node-id="9:2055">
        <p className="flex-[1_0_0] font-[family-name:var(--sds-typography-heading-font-family,'Inter:Semi_Bold',sans-serif)] font-[var(--sds-typography-heading-font-weight,600)] leading-[1.2] min-h-px min-w-px not-italic relative shrink-0 text-[color:var(--sds-color-text-default-default,#1e1e1e)] text-[length:var(--sds-typography-heading-size-base,24px)] tracking-[-0.48px] whitespace-pre-wrap" data-node-id="I9:2055;2087:8466">
          "Quote"
        </p>
      </div>
      <div className="content-stretch flex gap-[var(--sds-size-space-300,12px)] items-start relative shrink-0 w-[139px]" data-name="Avatar Block" data-node-id="9:2056">
        <Avatar className="overflow-clip relative rounded-[var(--sds-size-radius-full,9999px)] shrink-0 size-[40px]" />
        <div className="content-stretch flex flex-[1_0_0] flex-col gap-[var(--sds-size-space-050,2px)] items-start leading-[0] min-h-px min-w-px not-italic relative shrink-0 text-[length:var(--sds-typography-body-size-medium,16px)]" data-name="Info" data-node-id="I9:2056;2010:15577">
          <div className="flex flex-col font-[family-name:var(--sds-typography-body-font-family,'Inter:Semi_Bold',sans-serif)] font-[var(--sds-typography-body-font-weight-strong,600)] justify-center relative shrink-0 text-[color:var(--sds-color-text-default-secondary,#757575)] w-full" data-node-id="I9:2056;2010:15578">
            <p className="leading-[1.4] whitespace-pre-wrap">Title</p>
          </div>
          <div className="flex flex-col font-[family-name:var(--sds-typography-body-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-body-font-weight-regular,400)] justify-center relative shrink-0 text-[color:var(--sds-color-text-default-tertiary,#b3b3b3)] w-full" data-node-id="I9:2056;2010:15579">
            <p className="leading-[1.4] whitespace-pre-wrap">Description</p>
          </div>
        </div>
      </div>
    </div>
  );
}
type TextContentHeadingProps = {
  className?: string;
  hasSubheading?: boolean;
  heading?: string;
  subheading?: string;
  align?: "Start";
};

function TextContentHeading({ className, hasSubheading = true, heading = "Heading", subheading = "Subheading", align = "Start" }: TextContentHeadingProps) {
  return (
    <div className={className} data-name="Align=Start" data-node-id="9:2035">
      <p className="font-[family-name:var(--sds-typography-heading-font-family,'Inter:Semi_Bold',sans-serif)] font-[var(--sds-typography-heading-font-weight,600)] leading-[1.2] relative shrink-0 text-[color:var(--sds-color-text-default-default,#1e1e1e)] text-[length:var(--sds-typography-heading-size-base,24px)] tracking-[-0.48px] w-full whitespace-pre-wrap" data-node-id="9:2037">
        {heading}
      </p>
      {hasSubheading && (
        <div className="flex flex-col font-[family-name:var(--sds-typography-subheading-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-subheading-font-weight,400)] justify-center leading-[0] relative shrink-0 text-[color:var(--sds-color-text-default-secondary,#757575)] text-[length:var(--sds-typography-subheading-size-medium,20px)] w-full" data-node-id="9:2038">
          <p className="leading-[1.2] whitespace-pre-wrap">{subheading}</p>
        </div>
      )}
    </div>
  );
}
type ButtonGroupProps = {
  className?: string;
  buttonStart?: boolean;
  buttonEnd?: boolean;
  align?: "Justify";
};

function ButtonGroup({ className, buttonStart = true, buttonEnd = true, align = "Justify" }: ButtonGroupProps) {
  return (
    <div className={className} data-name="Align=Justify" data-node-id="9:2002">
      {buttonStart && (
        <div className="box-border content-stretch flex flex-[1_0_0] gap-[var(--sds-size-space-200,8px)] items-center justify-center min-h-px min-w-px overflow-clip p-[var(--sds-size-space-300,12px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" data-name="Button" data-node-id="9:2010">
          <p className="font-[family-name:var(--sds-typography-body-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-body-font-weight-regular,400)] leading-none not-italic relative shrink-0 text-[color:var(--sds-color-text-neutral-default,#303030)] text-[length:var(--sds-typography-body-size-medium,16px)]" data-node-id="I9:2010;9762:5145">
            Button
          </p>
        </div>
      )}
      {buttonEnd && (
        <div className="bg-[var(--sds-color-background-brand-default,#2c2c2c)] border-[var(--sds-color-border-brand-default,#2c2c2c)] border-[var(--sds-size-stroke-border,1px)] border-solid flex-[1_0_0] min-h-px min-w-px relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" data-name="Button" data-node-id="9:2011">
          <div className="box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center overflow-clip p-[var(--sds-size-space-300,12px)] relative rounded-[inherit] w-full">
            <p className="font-[family-name:var(--sds-typography-body-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-body-font-weight-regular,400)] leading-none not-italic relative shrink-0 text-[color:var(--sds-color-text-brand-on-brand,#f5f5f5)] text-[length:var(--sds-typography-body-size-medium,16px)]" data-node-id="I9:2011;9762:429">
              Button
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
type TextContentTitleProps = {
  className?: string;
  subtitle?: string;
  hasSubtitle?: boolean;
  title?: string;
  align?: "Center";
};

function TextContentTitle({ className, subtitle = "Subtitle", hasSubtitle = true, title = "Title", align = "Center" }: TextContentTitleProps) {
  return (
    <div className={className} data-name="Align=Center" data-node-id="9:1992">
      <p className="font-[family-name:var(--sds-typography-title-hero-font-family,'Inter:Bold',sans-serif)] font-[var(--sds-typography-title-hero-font-weight,700)] leading-[1.2] relative shrink-0 text-[color:var(--sds-color-text-default-default,#1e1e1e)] text-[length:var(--sds-typography-title-hero-size,72px)] tracking-[-2.16px] w-full whitespace-pre-wrap" data-node-id="9:1995">
        {title}
      </p>
      {hasSubtitle && (
        <div className="flex flex-col font-[family-name:var(--sds-typography-subtitle-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-subtitle-font-weight,400)] justify-center leading-[0] relative shrink-0 text-[color:var(--sds-color-text-default-secondary,#757575)] text-[length:var(--sds-typography-subtitle-size-base,32px)] w-full" data-node-id="9:1996">
          <p className="leading-[1.2] whitespace-pre-wrap">{subtitle}</p>
        </div>
      )}
    </div>
  );
}
type HeaderAuthProps = {
  className?: string;
  state?: "Logged Out";
};

function HeaderAuth({ className, state = "Logged Out" }: HeaderAuthProps) {
  return (
    <div className={className} data-name="State=Logged Out" data-node-id="9:1924">
      <div className="bg-[var(--sds-color-background-neutral-tertiary,#e3e3e3)] border-[var(--sds-color-border-neutral-secondary,#767676)] border-[var(--sds-size-stroke-border,1px)] border-solid flex-[1_0_0] min-h-px min-w-px relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" data-name="Button" data-node-id="9:1927">
        <div className="box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center overflow-clip p-[var(--sds-size-space-200,8px)] relative rounded-[inherit] w-full">
          <p className="font-[family-name:var(--sds-typography-body-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-body-font-weight-regular,400)] leading-none not-italic relative shrink-0 text-[color:var(--sds-color-text-default-default,#1e1e1e)] text-[length:var(--sds-typography-body-size-medium,16px)]" data-node-id="I9:1927;34:12129">
            Sign in
          </p>
        </div>
      </div>
      <div className="bg-[var(--sds-color-background-brand-default,#2c2c2c)] border-[var(--sds-color-border-brand-default,#2c2c2c)] border-[var(--sds-size-stroke-border,1px)] border-solid flex-[1_0_0] min-h-px min-w-px relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" data-name="Button" data-node-id="9:1928">
        <div className="box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center overflow-clip p-[var(--sds-size-space-200,8px)] relative rounded-[inherit] w-full">
          <p className="font-[family-name:var(--sds-typography-body-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-body-font-weight-regular,400)] leading-none not-italic relative shrink-0 text-[color:var(--sds-color-text-brand-on-brand,#f5f5f5)] text-[length:var(--sds-typography-body-size-medium,16px)]" data-node-id="I9:1928;34:12125">
            Register
          </p>
        </div>
      </div>
    </div>
  );
}
type NavigationPillProps = {
  className?: string;
  label?: string;
  state?: "Default" | "Active";
};

function NavigationPill({ className, label = "Link", state = "Default" }: NavigationPillProps) {
  if (state === "Active") {
    return (
      <div className={className} data-name="State=Active" data-node-id="9:1752">
        <div className="flex flex-col font-[family-name:var(--sds-typography-body-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-body-font-weight-regular,400)] justify-center leading-[0] not-italic relative shrink-0 text-[color:var(--sds-color-text-brand-on-brand-secondary,#1e1e1e)] text-[length:var(--sds-typography-body-size-medium,16px)] whitespace-nowrap" data-node-id="9:1755">
          <p className="leading-none">{label}</p>
        </div>
      </div>
    );
  }
  return (
    <div className={className} data-name="State=Default" data-node-id="9:1753">
      <div className="flex flex-col font-[family-name:var(--sds-typography-body-font-family,'Inter:Regular',sans-serif)] font-[var(--sds-typography-body-font-weight-regular,400)] justify-center leading-[0] not-italic relative shrink-0 text-[color:var(--sds-color-text-default-default,#1e1e1e)] text-[length:var(--sds-typography-body-size-medium,16px)] whitespace-nowrap" data-node-id="9:1756">
        <p className="leading-none">{label}</p>
        </div>
      </div>
    );
  }
}
type NavigationPillListProps = {
  className?: string;
  link6?: boolean;
  link2?: boolean;
  link5?: boolean;
  link4?: boolean;
  link3?: boolean;
  link1?: boolean;
  link7?: boolean;
  direction?: "Row" | "Column";
};

function NavigationPillList({ className, link6 = true, link2 = true, link5 = true, link4 = true, link3 = true, link1 = true, link7 = true, direction = "Row" }: NavigationPillListProps) {
  return (
    <div className={className} data-name="Direction=Row" data-node-id="9:1759">
      {link1 && <NavigationPill className="bg-[var(--sds-color-background-brand-tertiary,#f5f5f5)] box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center p-[var(--sds-size-space-200,8px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" state="Active" />}
      {link2 && <NavigationPill className="box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center p-[var(--sds-size-space-200,8px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />}
      {link3 && <NavigationPill className="box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center p-[var(--sds-size-space-200,8px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />}
      {link4 && <NavigationPill className="box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center p-[var(--sds-size-space-200,8px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />}
      {link5 && <NavigationPill className="box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center p-[var(--sds-size-space-200,8px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />}
      {link6 && <NavigationPill className="box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center p-[var(--sds-size-space-200,8px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />}
      {link7 && <NavigationPill className="box-border content-stretch flex gap-[var(--sds-size-space-200,8px)] items-center justify-center p-[var(--sds-size-space-200,8px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />}
    </div>
  );
}

export default function Home() {
  return (
    <div className="bg-[var(--sds-color-background-default-default,#ffffff)] content-stretch flex flex-col items-start relative size-full" data-name="Home" data-node-id="9:2708">
      <div className="bg-[var(--sds-color-background-default-default,#ffffff)] border-[var(--sds-color-border-default-default,#d9d9d9)] border-b-[var(--sds-size-stroke-border,1px)] border-l-0 border-r-0 border-solid border-t-0 relative shrink-0 w-full" data-name="Header" data-node-id="9:2709">
        <div className="box-border content-center flex flex-wrap gap-[var(--sds-size-space-600,0px24px)] items-center overflow-clip p-[var(--sds-size-space-800,32px)] relative rounded-[inherit] w-full">
          <div className="content-stretch flex gap-[24px] items-center relative shrink-0" data-name="Block" data-node-id="I9:2709;2299:23057">
            <div className="h-[35px] relative shrink-0 w-[40px]" data-name="Figma" data-node-id="I9:2709;189:26921">
              <div className="absolute bottom-[-5%] left-0 right-0 top-[-5%]">
                <img alt="" className="block max-w-none size-full" src={img} />
              </div>
            </div>
          </div>
          <NavigationPillList className="content-start flex flex-[1_0_0] flex-wrap gap-[var(--sds-size-space-200,8px)] items-start justify-end min-h-px min-w-px relative shrink-0" />
          <HeaderAuth className="content-stretch flex gap-[var(--sds-size-space-300,12px)] items-center relative shrink-0 w-[178px]" />
        </div>
      </div>
      <div className="bg-[var(--sds-color-background-default-secondary,#f5f5f5)] box-border content-stretch flex flex-col gap-[var(--sds-size-space-800,32px)] items-center px-[var(--sds-size-space-600,24px)] py-[var(--sds-size-space-4000,160px)] relative shrink-0 w-full" data-name="Hero Actions" data-node-id="9:2710">
        <TextContentTitle className="content-stretch flex flex-col gap-[var(--sds-size-space-200,8px)] items-center not-italic relative shrink-0 text-center" />
        <ButtonGroup className="content-stretch flex gap-[var(--sds-size-space-400,16px)] items-center relative shrink-0 w-[240px]" />
      </div>
      <div className="h-[400px] relative shrink-0 w-full" data-name="Section" data-node-id="9:2711">
        <div aria-hidden="true" className="absolute inset-0 pointer-events-none">
          <div className="absolute bg-[var(--sds-color-slate-200,#e3e3e3)] inset-0" />
          <img alt="" className="absolute max-w-none object-50%-50% object-contain opacity-20 size-full" src={imgSection} />
        </div>
      </div>
      <div className="bg-[var(--sds-color-background-default-default,#ffffff)] box-border content-stretch flex flex-col gap-[var(--sds-size-space-1200,48px)] items-start p-[var(--sds-size-space-1600,64px)] relative shrink-0 w-full" data-name="Card Grid Testimonials" data-node-id="9:2712">
        <TextContentHeading className="content-stretch flex flex-col gap-[var(--sds-size-space-200,8px)] items-start not-italic relative shrink-0" />
        <div className="content-start flex flex-wrap gap-[var(--sds-size-space-1200,48px)] items-start relative shrink-0 w-full" data-name="Card Grid" data-node-id="I9:2712;78:24784">
          <TestimonialCard className="bg-[var(--sds-color-background-default-default,#ffffff)] border-[var(--sds-color-border-default-default,#d9d9d9)] border-[var(--sds-size-stroke-border,1px)] border-solid box-border content-stretch flex flex-[1_0_0] flex-col gap-[var(--sds-size-space-600,24px)] items-start min-h-px min-w-[300px] p-[var(--sds-size-space-600,24px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />
          <TestimonialCard className="bg-[var(--sds-color-background-default-default,#ffffff)] border-[var(--sds-color-border-default-default,#d9d9d9)] border-[var(--sds-size-stroke-border,1px)] border-solid box-border content-stretch flex flex-[1_0_0] flex-col gap-[var(--sds-size-space-600,24px)] items-start min-h-px min-w-[300px] p-[var(--sds-size-space-600,24px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />
          <TestimonialCard className="bg-[var(--sds-color-background-default-default,#ffffff)] border-[var(--sds-color-border-default-default,#d9d9d9)] border-[var(--sds-size-stroke-border,1px)] border-solid box-border content-stretch flex flex-[1_0_0] flex-col gap-[var(--sds-size-space-600,24px)] items-start min-h-px min-w-[300px] p-[var(--sds-size-space-600,24px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />
          <TestimonialCard className="bg-[var(--sds-color-background-default-default,#ffffff)] border-[var(--sds-color-border-default-default,#d9d9d9)] border-[var(--sds-size-stroke-border,1px)] border-solid box-border content-stretch flex flex-[1_0_0] flex-col gap-[var(--sds-size-space-600,24px)] items-start min-h-px min-w-[300px] p-[var(--sds-size-space-600,24px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />
          <TestimonialCard className="bg-[var(--sds-color-background-default-default,#ffffff)] border-[var(--sds-color-border-default-default,#d9d9d9)] border-[var(--sds-size-stroke-border,1px)] border-solid box-border content-stretch flex flex-[1_0_0] flex-col gap-[var(--sds-size-space-600,24px)] items-start min-h-px min-w-[300px] p-[var(--sds-size-space-600,24px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />
          <TestimonialCard className="bg-[var(--sds-color-background-default-default,#ffffff)] border-[var(--sds-color-border-default-default,#d9d9d9)] border-[var(--sds-size-stroke-border,1px)] border-solid box-border content-stretch flex flex-[1_0_0] flex-col gap-[var(--sds-size-space-600,24px)] items-start min-h-px min-w-[300px] p-[var(--sds-size-space-600,24px)] relative rounded-[var(--sds-size-radius-200,8px)] shrink-0" />
        </div>
      </div>
      <div className="bg-[var(--sds-color-background-default-default,#ffffff)] border-[var(--sds-color-border-default-default,#d9d9d9)] border-b-0 border-l-0 border-r-0 border-solid border-t-[var(--sds-size-stroke-border,1px)] relative shrink-0 w-[1200px]" data-name="Footer" data-node-id="9:2713">
        <div className="box-border content-start flex flex-wrap gap-[var(--sds-size-space-400,16px)] items-start overflow-clip pb-[var(--sds-size-space-4000,160px)] pt-[var(--sds-size-space-800,32px)] px-[var(--sds-size-space-800,32px)] relative rounded-[inherit] w-[1200px]">
          <div className="content-stretch flex flex-col gap-[var(--sds-size-space-600,24px)] items-start min-w-[240px] relative shrink-0 w-[262px]" data-name="Title" data-node-id="I9:2713;9640:4285">
            <div className="h-[35px] relative shrink-0 w-[23.333px]" data-name="Figma" data-node-id="I9:2713;189:27064">
              <div className="absolute inset-[-5%_-7.5%]">
                <img alt="" className="block max-w-none size-full" src={img1} />
              </div>
            </div>
            <div className="content-stretch flex gap-[var(--sds-size-space-400,16px)] items-center relative shrink-0" data-name="Button List" data-node-id="I9:2713;78:26377">
              <div className="h-[24px] relative shrink-0 w-[23.98px]" data-name="X Logo" data-node-id="I9:2713;325:12862">
                <img alt="" className="block max-w-none size-full" src={img2} />
              </div>
              <div className="relative shrink-0 size-[24px]" data-name="Logo Instagram" data-node-id="I9:2713;325:12998">
                <img alt="" className="block max-w-none size-full" src={img3} />
              </div>
              <div className="relative shrink-0 size-[24px]" data-name="Logo YouTube" data-node-id="I9:2713;325:13119">
                <img alt="" className="block max-w-none size-full" src={img4} />
              </div>
              <div className="relative shrink-0 size-[24px]" data-name="LinkedIn" data-node-id="I9:2713;325:12716">
                <img alt="" className="block max-w-none size-full" src={img5} />
              </div>
            </div>
          </div>
          <TextLinkList className="content-stretch flex flex-col gap-[var(--sds-size-space-300,12px)] items-start relative shrink-0 w-[262px]" />
          <TextLinkList className="content-stretch flex flex-col gap-[var(--sds-size-space-300,12px)] items-start relative shrink-0 w-[262px]" />
          <TextLinkList className="content-stretch flex flex-col gap-[var(--sds-size-space-300,12px)] items-start relative shrink-0 w-[262px]" />
        </div>
      </div>
    </div>
  );
}