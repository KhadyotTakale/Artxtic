import Link from "next/link";
import Image from "next/image";

export default function HomePage() {
    return (
        <div className="font-display selection:bg-landing-primary selection:text-black">

            {/* Header & Hero Section */}
            <header className="fixed top-0 z-50 w-full border-b border-white/10 bg-black/80 backdrop-blur-md">
                <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-landing-primary text-3xl">layers</span>
                        <span className="text-2xl font-bold tracking-tight text-white">Artxtic</span>
                    </div>
                    <div className="hidden items-center gap-8 md:flex">
                        <a className="text-sm font-medium hover:text-landing-primary" href="#">Showcase</a>
                        <a className="text-sm font-medium hover:text-landing-primary" href="#">Features</a>
                        <a className="text-sm font-medium hover:text-landing-primary" href="#">Pricing</a>
                        <a className="text-sm font-medium hover:text-landing-primary" href="#">Resources</a>
                    </div>
                    <div className="flex items-center gap-4">
                        <Link href="/sign-in" className="hidden text-sm font-medium md:block">Log in</Link>
                        <Link href="/sign-up" className="rounded-lg bg-landing-primary px-5 py-2 text-sm font-bold text-black transition-transform hover:scale-105">
                            Start Creating Free
                        </Link>
                    </div>
                </nav>
            </header>
            <main className="pt-24">
                {/* Hero Section */}
                <section className="relative px-6 py-20 text-center lg:py-32">
                    <div className="mx-auto max-w-4xl">
                        <h1 className="text-5xl font-bold leading-tight tracking-tighter text-white md:text-7xl">
                            Generate stunning visuals <br />
                            <span className="text-landing-primary">(With just words)</span>
                        </h1>
                        <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400 md:text-xl">
                            Transform your wildest ideas into high-fidelity AI art in seconds. From photorealistic portraits to dreamlike landscapes, Artxtic brings your vision to life.
                        </p>
                        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
                            <Link href="/sign-up" className="inline-block text-center w-full rounded-xl bg-landing-primary px-8 py-4 text-lg font-bold text-black sm:w-auto">
                                Start Creating Free
                            </Link>
                            <button className="w-full rounded-xl border border-white/20 bg-white/5 px-8 py-4 text-lg font-bold text-white backdrop-blur-sm sm:w-auto">
                                View Gallery
                            </button>
                        </div>
                    </div>
                    {/* Scrolling Gallery */}
                    <div className="mt-20 overflow-hidden">
                        <div className="flex gap-4 overflow-x-auto pb-8 no-scrollbar px-6">
                            <div className="min-w-[300px] group relative overflow-hidden rounded-2xl">
                                <img className="aspect-[3/4] w-full object-cover transition-transform duration-500 group-hover:scale-110" alt="Abstract colorful 3D fluid art" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCxUZL66-HxD4MaEFSjfPnnAhAJQXym62Ua39gz5kRss9AxCdbDUXIk3RdqSbWs8fcjSLkMbHbGEq34Q9Uofwv4b6etMJ7NbovtKsJ2vqDPBQJDHHMhQ_VxjSal6-hcqHjWpKLaj-yEo58g3iilhPzLL2qf8uF4qZsCkwRhMGKByEDnRC8ym6Khnw-OGsEbmB_Pp0iTHiJChbB5R0-uglhn0UJr4CJi-PmsIAir7-63Bw2KhK2HZx-YGEZvN5kvc1kdR7_l-r2Ie1US" />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end text-left">
                                    <p className="text-xs font-bold uppercase tracking-widest text-landing-primary">Abstract</p>
                                    <p className="text-sm text-white">Neon Cyberpunk Dreams</p>
                                </div>
                            </div>
                            <div className="min-w-[300px] group relative overflow-hidden rounded-2xl">
                                <img className="aspect-[3/4] w-full object-cover transition-transform duration-500 group-hover:scale-110" alt="High fidelity cinematic landscape" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCjsdr923wcbqgEX5fBo4rl1wl-V6Go6UgW43Zx6QaQUAPlR0vFq_z2sAwz8ott7Fuwkr8dbX-Y3-e4AcNGK8TOxiCGBxHCEkUNzxwLd_spZfuxJWR_qdQah7pKEBM42Rrs__fdz3BfVL1xN1rEHrhZH5ZVp7BEwt1IdQlHSj8Lmv_n-3fEx0e7nUvN7k59rDKLDHOc875GOueK3v02tSgV4Wd0GIIO2kE-b7_ss7s7exempfxHuXxX3I9ZwQcDZBAa8GkeuGbZ4G5K" />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end text-left">
                                    <p className="text-xs font-bold uppercase tracking-widest text-landing-primary">Landscape</p>
                                    <p className="text-sm text-white">The Emerald Peaks</p>
                                </div>
                            </div>
                            <div className="min-w-[300px] group relative overflow-hidden rounded-2xl">
                                <img className="aspect-[3/4] w-full object-cover transition-transform duration-500 group-hover:scale-110" alt="Hyper-realistic portrait of a woman" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDVviN1tQGFwvGlRmp_qCmMXcjGykTAtfUvuSSzjBNyxk7qleKKkcRVrgNrGM0NsXIrGxs-UNVYX1Gghkt_57IyESGmraJPphpWBc4Md0XLkoI-Q2Ind3_CWVeUU-rIvthAVzLf2P8ckk9ip6JMtfAZJ_Nry9TVxTNDF9cGindGA7ePj0joK2RrrYSGyH-3uMFY4ne0wTJ3S-VxdDjobNJJFhgmvjk9G8p91ZrZdASf3feg5f0VPQOHsi5LdATuGnU2_lPPE3uXNpYR" />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end text-left">
                                    <p className="text-xs font-bold uppercase tracking-widest text-landing-primary">Portrait</p>
                                    <p className="text-sm text-white">Human Essence v2.0</p>
                                </div>
                            </div>
                            <div className="min-w-[300px] group relative overflow-hidden rounded-2xl">
                                <img className="aspect-[3/4] w-full object-cover transition-transform duration-500 group-hover:scale-110" alt="Futuristic sci-fi city concept art" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBT4ihgFeZUCBSR8mCokdRs-1Oo9EQSRzPY-v8Y2vwwTMs-yhlxXeNIwiOWidQmsFP6RD1UTZ-hkrxipKBJGV27_Qh5oQtNWPiovckmxcEW7wVvpnQifpTEtOaywTsPByoFCStw47wp8YErQF3esZAzATENx5O8wlrxqNFKPw03EKtTrA2G7-M5ZdEIS6MFdfW8VszxEbs8I4See4kV7uNVVXmKVU31T9nxR0DX-pHAkh-ZyjtZP9H4Y6FqZrp-peDFIQWW5TibXcXS" />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end text-left">
                                    <p className="text-xs font-bold uppercase tracking-widest text-landing-primary">Futuristic</p>
                                    <p className="text-sm text-white">Orbital Station Alpha</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                {/* Video Section */}
                <section className="bg-neutral-dark/50 px-6 py-24">
                    <div className="mx-auto max-w-7xl flex flex-col md:flex-row items-center gap-12">
                        <div className="flex-1">
                            <h2 className="text-4xl font-bold text-white mb-6">How does it work?</h2>
                            <p className="text-slate-400 text-lg mb-8">Watch how easy it is to generate professional-grade assets with a single sentence. Our engine processes natural language to understand style, lighting, and composition.</p>
                            <div className="flex items-center gap-4 text-landing-primary">
                                <span className="material-symbols-outlined text-4xl">trending_flat</span>
                                <span className="text-xl font-medium">See the magic in 60 seconds</span>
                            </div>
                        </div>
                        <div className="flex-1 w-full">
                            <div className="group relative aspect-video overflow-hidden rounded-2xl border border-white/10">
                                <img className="h-full w-full object-cover opacity-60" alt="Tech studio setup with large monitors" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAzX0zyhaMLJ4kCwLXi56MiHk0dVTrXXfANrrWi_miJolVTmPdvV_j2gWQr5faUyTa8KWz_XLB1MJnUsm52Oc28yk2WmKvMLa5un8W8TSiIaxSnSOg-Y3ZSeyjdO0i-QHWtpvGhApt7EwFZgI9tdAGF67QOujiL_0nb72NWCLkLpYtBO7DX9F4jZysWy21weopIzF6MtG6HuUYwL8v_097usdZ3Hkm4PtKAfGqpc66VfPcdTNViFWc5xaEilJCgzeluP1s0UHjfKYf3" />
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <button className="flex h-20 w-20 items-center justify-center rounded-full bg-landing-primary text-black transition-transform group-hover:scale-110">
                                        <span className="material-symbols-outlined text-4xl fill-current">play_arrow</span>
                                    </button>
                                </div>
                                <div className="absolute bottom-4 left-4 right-4 flex h-1.5 rounded-full bg-white/20">
                                    <div className="h-full w-1/3 rounded-full bg-landing-primary"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                {/* Showcase Section */}
                <section className="px-6 py-24">
                    <div className="mx-auto max-w-7xl">
                        <div className="text-center mb-16">
                            <h2 className="text-4xl font-bold text-white mb-4">AI that adapts to your vision</h2>
                            <div className="flex flex-wrap justify-center gap-2 mt-8">
                                <button className="rounded-full bg-landing-primary px-6 py-2 text-sm font-bold text-black">Images</button>
                                <button className="rounded-full bg-white/5 border border-white/10 px-6 py-2 text-sm font-medium hover:bg-white/10">Videos</button>
                                <button className="rounded-full bg-white/5 border border-white/10 px-6 py-2 text-sm font-medium hover:bg-white/10">Models</button>
                                <button className="rounded-full bg-white/5 border border-white/10 px-6 py-2 text-sm font-medium hover:bg-white/10">Advanced</button>
                            </div>
                        </div>
                        {/* Dashboard Mockup */}
                        <div className="rounded-2xl border border-white/10 bg-[#0a0a0a] p-4 shadow-2xl md:p-8">
                            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                                <div className="lg:col-span-1 flex flex-col gap-6">
                                    <div>
                                        <label className="text-xs font-bold uppercase tracking-wider text-slate-500">Prompt</label>
                                        <textarea className="mt-2 w-full rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-white focus:border-landing-primary focus:ring-0" rows={4} defaultValue="A cyberpunk samurai standing in the rain of Neo-Tokyo, 8k resolution, cinematic lighting, dramatic shadows --v 6.0" />
                                    </div>
                                    <div>
                                        <label className="text-xs font-bold uppercase tracking-wider text-slate-500">Aspect Ratio</label>
                                        <div className="mt-2 grid grid-cols-3 gap-2">
                                            <button className="rounded-lg border border-landing-primary bg-landing-primary/10 py-2 text-xs font-bold text-landing-primary">16:9</button>
                                            <button className="rounded-lg border border-white/10 py-2 text-xs text-slate-400">1:1</button>
                                            <button className="rounded-lg border border-white/10 py-2 text-xs text-slate-400">9:16</button>
                                        </div>
                                    </div>
                                    <button className="mt-4 w-full rounded-xl bg-landing-primary py-3 font-bold text-black">Generate</button>
                                </div>
                                <div className="lg:col-span-3 grid grid-cols-2 gap-4">
                                    <img className="rounded-xl object-cover h-full w-full" alt="AI generated cyberpunk fashion" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAArYuVV_vaw53rJ05EFl3ubhyoO8fKVtAeRbbEBbgYO5fJlnzRF3hJHhahw2uLluI0l-nu6W8UcwJh0uMwezLwVt3Rc4nlUL25jlpGtHSCPOJk4pjFSD4q1VSQiPCOIYcwkZT_jGzktxBUHgBLdaVQL57XvCn9Xl6utAu_U06_9t03UHUTXZCHkCaKoQhrY-XqAgDuxlo7sNvTmYpQHO0j0C7Wga7A025Ro9guPEwzG-by9274XLn7J2Ol2U6QPpCk37IpkF-V2LrG" />
                                    <img className="rounded-xl object-cover h-full w-full" alt="Vibrant digital color pattern" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCWTpyljPLduslZurQ3jFFpBJY17xM-WI722A6rd5a-kosuGBG1ZpjaAbEctH91VtbkOgwklawFXkZ5VKfZP6HtFHHOTo-DQshB3Hm2yv6UU_mJ7usJQI986MRc0s2fdYV0w7O9HV8_cMBOvlmSvzLM19-qLKcKyC-5m_-ymdHNtImt9zhSibD-YJQsqzFCdYOCr55oUk5YDJhAjv8xvZ7KGkS2au4bdDgYst70zMr97JjbukEK3RgS8S4_qAK7riKUA9REQValKzjj" />
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                {/* Gallery Masonry */}
                <section className="bg-neutral-dark/30 px-6 py-24">
                    <div className="mx-auto max-w-7xl">
                        <h2 className="text-4xl font-bold text-white mb-12">Made with Artxtic</h2>
                        <div className="masonry-grid">
                            <div className="masonry-item-large group relative overflow-hidden rounded-xl">
                                <img className="h-full w-full object-cover" alt="Abstract classical art style painting" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC1LV8iggMO-QcQjc1dXj223kULpzUatotkv6A0ITcWrlefarS71k2kxuWOZgk-GLcB8-LJw_lJ9jZl1X4uHIMTQYIVEPBY4SEoJU2_V0kqhj5a9o12pY9bZZ4Yi5YfMgdCLfyaLFfAPVj8ihtKdYfoZKjllyFr8ceYDvAg8Uzc-BSK5v6Ixb4m0rKvlTS8JxMJEgg2rpNXG-WeugxDfg09lvBdKZN5HXnARtqI2YnKQIpFsBc8RvHBeqZM7YzOzftuExI2Wjq6Xc5S" />
                                <div className="absolute inset-0 flex items-end bg-black/60 opacity-0 transition-opacity group-hover:opacity-100 p-4">
                                    <p className="text-xs text-white">"Renaissance cyborg in a golden garden..."</p>
                                </div>
                            </div>
                            <div className="group relative overflow-hidden rounded-xl">
                                <img className="h-full w-full object-cover" alt="Minimalist abstract curves" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCdENvqAHWkOAKz6cd7LuXFmHLKA8_8zmmKb4aTLFb-_fomBoiPUhsYRqaIrv5E_sZ1_vYM4CSNsOzZphZzX3nRFTslTSq-2EMbV6MkymNSb450VSPmuTQVtigh0Srm0674jUIQr8WAibbanSQzRsFyfvIqwV9ylk8uj8dcobAV8VAH86H4G0z89M21ZsnwB24VokyD6-T8k7FMxGQKXvmGGRgwTWevMlvIAG8JhNQ6p-mKuok4tim-hd7Mfvd9hje8sSOqakgiE7ZP" />
                            </div>
                            <div className="masonry-item-wide group relative overflow-hidden rounded-xl">
                                <img className="h-full w-full object-cover" alt="Misty mountain forest landscape" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDIMhxcNk-P542BbP6ZS6K78S-ZPdeD5tzJbilFVP40YJSqZYH-D7okqXlzjOEKm8miQ1Lgxcm4VBjSDVOKwCmmpZLViSlN7PaLWrOf8bfesWD8af0JhxmpAsMMbI29QQgkKgmscxfyyPE1VbZWxPwGEo8-boPuuF_bl_rjmV9-yKBH9K4W1O1lvtQGF5rAwwoUFKQIdlO4PgXw4fFMJan5B7rKbH1ReKTOIHAKYWa2CPyUBtIzoluG5Z9bkiJDifD989e20DRWwsNp" />
                            </div>
                            <div className="bg-landing-primary p-6 rounded-xl flex flex-col justify-between">
                                <span className="material-symbols-outlined text-4xl text-black">format_quote</span>
                                <p className="text-black font-medium">"Artxtic completely changed our design workflow. We go from concept to final visual in minutes."</p>
                                <div className="mt-4">
                                    <p className="text-sm font-bold text-black">Sarah Chen</p>
                                    <p className="text-xs text-black/60">Creative Director, Flux</p>
                                </div>
                            </div>
                            <div className="group relative overflow-hidden rounded-xl">
                                <img className="h-full w-full object-cover" alt="3D tech abstract visualization" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDAn_gqQwUmQ7GSvzAK2qFw8cDOBpZak779kmPzjqgYx3ZscJRJku3-26BcJbKu-UdYFIrPCt1Akdi5oqT1H4gC6NI-PX9wTk4XF_Pcoypb0N0KIoIunPkjNNO01Q1wUxjls6wBNw1kEh4VC0hDmz1jC2YIAs6P_ttpq7dUYKEHCNLdKCrooSIJ9ssD05SgDL-BfiS_1PBTYTWT2mzUVs8j7plrjvHJTPxu6t8IbipX0ejg84DMwPJn29Rxd5qJX7nQe9GdzkeNXkRt" />
                            </div>
                        </div>
                    </div>
                </section>
                {/* Features Section */}
                <section className="px-6 py-24">
                    <div className="mx-auto max-w-7xl">
                        <h2 className="text-4xl font-bold text-white mb-16 text-center">Powering the next generation of creators</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {/* Feature Card 1 */}
                            <div className="rounded-2xl border border-white/10 bg-white/5 p-8 hover:border-landing-primary/50 transition-colors">
                                <span className="material-symbols-outlined text-landing-primary text-4xl mb-4">bolt</span>
                                <h3 className="text-xl font-bold text-white mb-2">Instant Gen</h3>
                                <p className="text-slate-400">High-speed rendering that delivers 4 unique variations in under 30 seconds.</p>
                            </div>
                            {/* Feature Card 2 */}
                            <div className="rounded-2xl border border-white/10 bg-white/5 p-8 hover:border-landing-primary/50 transition-colors">
                                <span className="material-symbols-outlined text-landing-primary text-4xl mb-4">model_training</span>
                                <h3 className="text-xl font-bold text-white mb-2">Multiple Models</h3>
                                <p className="text-slate-400">Switch between Stable Diffusion, Midjourney API, and our custom Artxtic-v4.</p>
                            </div>
                            {/* Feature Card 3 */}
                            <div className="rounded-2xl border border-white/10 bg-white/5 p-8 hover:border-landing-primary/50 transition-colors">
                                <span className="material-symbols-outlined text-landing-primary text-4xl mb-4">folder_special</span>
                                <h3 className="text-xl font-bold text-white mb-2">Your Library</h3>
                                <p className="text-slate-400">Cloud-synced storage for all your generations, sorted and searchable.</p>
                            </div>
                            {/* Feature Card 4 */}
                            <div className="rounded-2xl border border-white/10 bg-white/5 p-8 hover:border-landing-primary/50 transition-colors">
                                <span className="material-symbols-outlined text-landing-primary text-4xl mb-4">aspect_ratio</span>
                                <h3 className="text-xl font-bold text-white mb-2">Flexible Formats</h3>
                                <p className="text-slate-400">Export in PNG, WebP, or high-res TIFF with custom aspect ratios up to 8K.</p>
                            </div>
                            {/* Feature Card 5 */}
                            <div className="rounded-2xl border border-white/10 bg-white/5 p-8 hover:border-landing-primary/50 transition-colors">
                                <span className="material-symbols-outlined text-landing-primary text-4xl mb-4">share</span>
                                <h3 className="text-xl font-bold text-white mb-2">Download &amp; Share</h3>
                                <p className="text-slate-400">Direct integration with Figma, Adobe CC, and social platforms.</p>
                            </div>
                            {/* Feature Card 6 */}
                            <div className="rounded-2xl border border-white/10 bg-white/5 p-8 hover:border-landing-primary/50 transition-colors">
                                <span className="material-symbols-outlined text-landing-primary text-4xl mb-4">bar_chart</span>
                                <h3 className="text-xl font-bold text-white mb-2">Usage Tracking</h3>
                                <p className="text-slate-400">Detailed analytics on token usage, generation costs, and storage limits.</p>
                            </div>
                        </div>
                    </div>
                </section>
                {/* Compatibility Section */}
                <section className="flex flex-col lg:flex-row min-h-[600px]">
                    <div className="lg:w-1/2 relative min-h-[400px]">
                        <div className="absolute inset-0 grid grid-cols-2 gap-2 p-4">
                            <img className="h-full w-full object-cover rounded-lg" alt="Blue abstract wave texture" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDYIMAlBZQ_WnnT5aVtHEe0ykhxhIV964q-Os_z6JrsMPF-cDAe0tACEOTLaDjAzsG5D9BN5gDgdPJ2kyB1rmlXMUPsxMGzUPrQizeCorO1zG5BS4f2YrI-3Lm8CRkQ3jRkxdqRTLgWNa8EMH5zmfO1JK1OIvKBnNenXFrA81gEUAkxOh4av1f8ag9ceJjqIdPhHnJSCsBMTn_3lQRmljPxuVsJYT_5kXdYolARmAa3plCF0Q4HYLWY-HyoeVhjiNbEjUM9N1k1m7eL" />
                            <img className="h-full w-full object-cover rounded-lg" alt="Geometric black and white art" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBjn88LQGziGC9tHkLNE2Ipw1CCK6dY_JY4hjAAWP-__zdgZwiLgXK6RjkzvTbSkOEmlljC6H-4G7H2AdTSLFwYBhmBDEoUFX4v2x73RO3uqknbWzutiaAS5EHbF-sEPG5VjM2iX44pWJ9mUUZliSiGwesfBFyrHaoWSqgJb7Xq6j6v5bKAFRhhnKGkoj_AYT9tzs5S1NeKZuXnWCUVfqJjJuyg-KJOJqw-Iyrgpa7rTPStZFrD6IO2wFgcB7lXVStJUjOTpmKUKBAy" />
                            <img className="h-full w-full object-cover rounded-lg" alt="Soft pink and blue gradient" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDGmL69Q3erGWujOEfWAW1zVLS3WcdbENh6RJK4HbsEG7hxAaoNyBHmKnXUSqGtqRF0qpPTJ65Y9_P0DBNJEspTR42nf1tNJZ3ssQ4ho-SJHp6i-8h0rlvbdljLekXxvfOAEIS-rNhziBbadFMnHMpiHrHGCqm_t519llxNkXsso4XSinX2pE23kyE4JEQMwS2w1jwOElQuxlPtdeMt4iq3xSEz2wEN19X_A5L0drgf9461KvyPGeOtJjm5zz8M9fOt44tp4K7RixAX" />
                            <img className="h-full w-full object-cover rounded-lg" alt="Complex digital color abstraction" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAlmJO9Iygjmmkrtch34TalOPKEsBzW2BQADn5Wi5QOHvoXho6ZBvMmtZoQO0ZRMTgC2zIAIwBFmXcL78-wuuplKdF1-bdQq3Nr3XUceW9yca0EitsdLE9AT2ybdEDvaIzMFoaxlj7sGL91jR9Cd7_GXkv8D5pbJ6XtvuTclML_-Yhf6YRFQNYZvei3JNgaI1N5uJuoH7039VaB2ipjuaoIuNnoTwjWh5d2btZeJxDyWjGfCa02ajLfhc0E8sDCfWgzCWdL1BK2O8xs" />
                        </div>
                    </div>
                    <div className="lg:w-1/2 bg-landing-primary flex flex-col justify-center px-8 py-20 lg:px-24">
                        <h2 className="text-5xl font-bold text-black mb-6">Your ideas are welcome here</h2>
                        <p className="text-black/80 text-xl mb-10">Whether you're a professional designer, an aspiring artist, or a business owner, Artxtic scales with your creativity. No steep learning curves, just pure inspiration.</p>
                        <button className="w-fit rounded-xl bg-black px-10 py-4 text-lg font-bold text-white transition-transform hover:scale-105">
                            Explore Capabilities
                        </button>
                    </div>
                </section>
                {/* Pricing Section */}
                <section className="px-6 py-24">
                    <div className="mx-auto max-w-7xl">
                        <div className="text-center mb-16">
                            <h2 className="text-4xl font-bold text-white">Simple, transparent pricing</h2>
                            <p className="mt-4 text-slate-400">Choose the plan that's right for your creative needs.</p>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            {/* Free Plan */}
                            <div className="rounded-3xl border border-white/10 bg-white/5 p-8 flex flex-col">
                                <h3 className="text-xl font-bold text-white mb-2">Free</h3>
                                <div className="text-3xl font-bold text-white mb-6">$0<span className="text-lg font-normal text-slate-500">/mo</span></div>
                                <ul className="space-y-4 mb-8 flex-1">
                                    <li className="flex items-center gap-2 text-sm text-slate-400"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> 50 generations / month</li>
                                    <li className="flex items-center gap-2 text-sm text-slate-400"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> Standard speed</li>
                                    <li className="flex items-center gap-2 text-sm text-slate-400"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> Public gallery</li>
                                </ul>
                                <button className="w-full rounded-xl border border-white/20 py-3 text-sm font-bold text-white">Get Started</button>
                            </div>
                            {/* Pro Plan */}
                            <div className="rounded-3xl border-2 border-landing-primary bg-landing-primary/5 p-8 flex flex-col scale-105 shadow-[0_0_30px_rgba(191,255,0,0.15)]">
                                <div className="bg-landing-primary text-black text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full w-fit mb-4">Most Popular</div>
                                <h3 className="text-xl font-bold text-white mb-2">Pro</h3>
                                <div className="text-3xl font-bold text-white mb-6">$29<span className="text-lg font-normal text-slate-500">/mo</span></div>
                                <ul className="space-y-4 mb-8 flex-1">
                                    <li className="flex items-center gap-2 text-sm text-slate-200"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> Unlimited generations</li>
                                    <li className="flex items-center gap-2 text-sm text-slate-200"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> Turbo processing</li>
                                    <li className="flex items-center gap-2 text-sm text-slate-200"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> Private mode &amp; Commercial rights</li>
                                    <li className="flex items-center gap-2 text-sm text-slate-200"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> 4K Upscaling</li>
                                </ul>
                                <button className="w-full rounded-xl bg-landing-primary py-3 text-sm font-bold text-black shadow-lg shadow-landing-primary/20">Upgrade Now</button>
                            </div>
                            {/* Enterprise Plan */}
                            <div className="rounded-3xl border border-white/10 bg-white/5 p-8 flex flex-col">
                                <h3 className="text-xl font-bold text-white mb-2">Enterprise</h3>
                                <div className="text-3xl font-bold text-white mb-6">Custom</div>
                                <ul className="space-y-4 mb-8 flex-1">
                                    <li className="flex items-center gap-2 text-sm text-slate-400"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> Team collaboration</li>
                                    <li className="flex items-center gap-2 text-sm text-slate-400"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> Dedicated GPU instance</li>
                                    <li className="flex items-center gap-2 text-sm text-slate-400"><span className="material-symbols-outlined text-landing-primary text-sm">check</span> SSO &amp; Custom API</li>
                                </ul>
                                <button className="w-full rounded-xl border border-white/20 py-3 text-sm font-bold text-white">Contact Sales</button>
                            </div>
                        </div>
                    </div>
                </section>
                {/* Stats Section */}
                <section className="bg-white/5 border-y border-white/10 py-12">
                    <div className="mx-auto max-w-7xl px-6 flex flex-col md:flex-row justify-around items-center gap-8">
                        <div className="text-center">
                            <p className="text-4xl font-bold text-landing-primary mb-1">10,000+</p>
                            <p className="text-slate-400 font-medium">images generated daily</p>
                        </div>
                        <div className="h-12 w-px bg-white/10 hidden md:block"></div>
                        <div className="text-center">
                            <p className="text-4xl font-bold text-landing-primary mb-1">5,000+</p>
                            <p className="text-slate-400 font-medium">happy creators</p>
                        </div>
                        <div className="h-12 w-px bg-white/10 hidden md:block"></div>
                        <div className="text-center">
                            <p className="text-4xl font-bold text-landing-primary mb-1">99.9%</p>
                            <p className="text-slate-400 font-medium">uptime performance</p>
                        </div>
                    </div>
                </section>
                {/* Final CTA Section */}
                <section className="px-6 py-24 relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-black via-background-dark to-landing-primary/20"></div>
                    <div className="relative mx-auto max-w-4xl text-center">
                        <h2 className="text-5xl font-bold text-white mb-6">Start creating today</h2>
                        <p className="text-xl text-slate-400 mb-10">Join the thousands of artists who are redefining the boundaries of digital media with Artxtic.</p>
                        <Link href="/sign-up" className="inline-block text-center rounded-xl bg-landing-primary px-12 py-5 text-xl font-bold text-black transition-all hover:scale-105 hover:shadow-[0_0_40px_rgba(191,255,0,0.3)]">
                            Start Creating Free
                        </Link>
                    </div>
                </section>
            </main>
            {/* Footer */}
            <footer className="border-t border-white/10 bg-black py-16 px-6">
                <div className="mx-auto max-w-7xl grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-12">
                    <div className="lg:col-span-2">
                        <div className="flex items-center gap-2 mb-6">
                            <span className="material-symbols-outlined text-landing-primary text-3xl">layers</span>
                            <span className="text-2xl font-bold text-white">Artxtic</span>
                        </div>
                        <p className="text-slate-400 max-w-xs mb-8">The world's most intuitive AI media generation platform. Professional tools for everyone.</p>
                        <div className="flex gap-4">
                            <a className="h-10 w-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-landing-primary hover:text-black transition-colors" href="#">
                                <span className="material-symbols-outlined">alternate_email</span>
                            </a>
                            <a className="h-10 w-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-landing-primary hover:text-black transition-colors" href="#">
                                <span className="material-symbols-outlined">public</span>
                            </a>
                            <a className="h-10 w-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-landing-primary hover:text-black transition-colors" href="#">
                                <span className="material-symbols-outlined">rss_feed</span>
                            </a>
                        </div>
                    </div>
                    <div>
                        <h4 className="text-white font-bold mb-6">Product</h4>
                        <ul className="space-y-4 text-slate-400 text-sm">
                            <li><a className="hover:text-landing-primary" href="#">Showcase</a></li>
                            <li><a className="hover:text-landing-primary" href="#">Features</a></li>
                            <li><a className="hover:text-landing-primary" href="#">Pricing</a></li>
                            <li><a className="hover:text-landing-primary" href="#">Models</a></li>
                        </ul>
                    </div>
                    <div>
                        <h4 className="text-white font-bold mb-6">Resources</h4>
                        <ul className="space-y-4 text-slate-400 text-sm">
                            <li><a className="hover:text-landing-primary" href="#">Documentation</a></li>
                            <li><a className="hover:text-landing-primary" href="#">API Reference</a></li>
                            <li><a className="hover:text-landing-primary" href="#">Community</a></li>
                            <li><a className="hover:text-landing-primary" href="#">Blog</a></li>
                        </ul>
                    </div>
                    <div>
                        <h4 className="text-white font-bold mb-6">Legal</h4>
                        <ul className="space-y-4 text-slate-400 text-sm">
                            <li><a className="hover:text-landing-primary" href="#">Terms of Service</a></li>
                            <li><a className="hover:text-landing-primary" href="#">Privacy Policy</a></li>
                            <li><a className="hover:text-landing-primary" href="#">Copyright Info</a></li>
                            <li><a className="hover:text-landing-primary" href="#">Cookie Settings</a></li>
                        </ul>
                    </div>
                </div>
                <div className="mx-auto max-w-7xl border-t border-white/10 mt-16 pt-8 text-center text-slate-500 text-xs">
                    © 2024 Artxtic AI. All rights reserved.
                </div>
            </footer>

        </div>
    );
}
